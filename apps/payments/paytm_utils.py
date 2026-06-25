import json
import uuid
import requests
import hashlib
import base64
from decimal import Decimal
from django.conf import settings
from Crypto.Cipher import AES
import logging

logger = logging.getLogger(__name__)


class PayTMGateway:
    """PayTM Payment Gateway Integration"""

    def __init__(self):
        self.mid = getattr(settings, "PAYTM_MID", "")
        self.merchant_key = getattr(settings, "PAYTM_MERCHANT_KEY", "")
        self.website_name = getattr(settings, "PAYTM_WEBSITE_NAME", "WEBSTAGING")
        self.industry_type = getattr(settings, "PAYTM_INDUSTRY_TYPE", "Retail")
        self.channel_id = getattr(settings, "PAYTM_CHANNEL_ID", "WEB")
        self.staging_url = "https://securestage.paytmpayments.com"
        self.production_url = "https://secure.paytmpayments.com"

    def is_staging(self):
        return getattr(settings, "PAYTM_DEBUG", True)

    def get_base_url(self):
        return self.staging_url if self.is_staging() else self.production_url

    def generate_checksum(self, params):
        """Generate checksum signature for PayTM"""
        # Sort parameters alphabetically
        sorted_params = sorted(params.items())

        # Create parameter string
        param_string = ""
        for key, value in sorted_params:
            if value is not None and value != "":
                param_string += f"{key}={value}&"

        param_string = param_string.rstrip("&")

        # Generate SHA256 hash with merchant key
        checksum_string = param_string + "|" + self.merchant_key
        return hashlib.sha256(checksum_string.encode()).hexdigest()

    def generate_checksum_v2(self, body_params):
        """Generate checksum for new PayTM API (body + head format)"""
        body_json = json.dumps(body_params)
        checksum = hashlib.sha256((body_json + self.merchant_key).encode()).hexdigest()
        return checksum

    def create_payment_request(
        self, order_id, amount, user_id, user_email, user_phone, callback_url
    ):
        """
        Create PayTM payment request
        Returns payment URL or form parameters
        """
        try:
            # Use new API format (body + head)
            body_params = {
                "requestType": "Payment",
                "mid": self.mid,
                "websiteName": self.website_name,
                "orderId": order_id,
                "callbackUrl": callback_url,
                "txnAmount": {
                    "value": str(amount),
                    "currency": "INR",
                },
                "userInfo": {
                    "custId": str(user_id),
                    "mobile": user_phone,
                    "email": user_email,
                },
            }

            # Generate checksum
            checksum = self.generate_checksum_v2(body_params)

            # Prepare request
            url = f"{self.get_base_url()}/theia/api/v1/initiateTransaction?mid={self.mid}&orderId={order_id}"
            headers = {"Content-Type": "application/json"}

            payload = {"body": body_params, "head": {"signature": checksum}}

            # Make API call
            response = requests.post(url, json=payload, headers=headers, timeout=30)

            if response.status_code == 200:
                response_data = response.json()
                result_code = (
                    response_data.get("body", {})
                    .get("resultInfo", {})
                    .get("resultCode")
                )

                if result_code == "0000":
                    payment_url = response_data.get("body", {}).get("paymentUrl")

                    return {
                        "success": True,
                        "payment_url": payment_url,
                        "merchant_transaction_id": order_id,
                        "form_params": None,
                    }
                else:
                    error_msg = (
                        response_data.get("body", {})
                        .get("resultInfo", {})
                        .get("resultMsg", "Unknown error")
                    )
                    return {"success": False, "error": error_msg}
            else:
                # Fallback to old API (form-based)
                return self.create_payment_request_legacy(
                    order_id, amount, user_id, user_email, user_phone, callback_url
                )

        except Exception as e:
            logger.error(f"PayTM initiation error: {str(e)}")
            return {"success": False, "error": str(e)}

    def create_payment_request_legacy(
        self, order_id, amount, user_id, user_email, user_phone, callback_url
    ):
        """Legacy form-based PayTM payment request (fallback)"""
        try:
            params = {
                "MID": self.mid,
                "ORDER_ID": order_id,
                "CUST_ID": str(user_id),
                "TXN_AMOUNT": str(amount),
                "CHANNEL_ID": self.channel_id,
                "WEBSITE": self.website_name,
                "INDUSTRY_TYPE_ID": self.industry_type,
                "CALLBACK_URL": callback_url,
                "EMAIL": user_email,
                "MOBILE_NO": user_phone,
            }

            # Generate checksum
            checksum = self.generate_checksum(params)
            params["CHECKSUMHASH"] = checksum

            return {
                "success": True,
                "form_params": params,
                "action_url": f"{self.get_base_url()}/theia/processTransaction",
                "merchant_transaction_id": order_id,
                "payment_url": None,
            }

        except Exception as e:
            logger.error(f"PayTM legacy initiation error: {str(e)}")
            return {"success": False, "error": str(e)}

    def verify_payment(self, merchant_transaction_id):
        """Verify payment status with PayTM"""
        try:
            # Prepare request
            url = f"{self.get_base_url()}/v3/order/status"
            headers = {"Content-Type": "application/json"}

            body_params = {"mid": self.mid, "orderId": merchant_transaction_id}

            checksum = self.generate_checksum_v2(body_params)

            payload = {"body": body_params, "head": {"signature": checksum}}

            response = requests.post(url, json=payload, headers=headers, timeout=30)

            if response.status_code == 200:
                response_data = response.json()
                body = response_data.get("body", {})
                result_info = body.get("resultInfo", {})
                result_code = result_info.get("resultCode")

                if result_code == "0000":
                    status = body.get("status", "")

                    return {
                        "success": True,
                        "status": status,
                        "transaction_id": body.get("txnId"),
                        "bank_txn_id": body.get("bankTxnId"),
                        "amount": body.get("txnAmount", {}).get("value"),
                        "payment_instrument": body.get("paymentInstrument", {}),
                    }
                else:
                    return {
                        "success": False,
                        "error": result_info.get("resultMsg", "Verification failed"),
                    }
            else:
                return {"success": False, "error": f"API Error: {response.status_code}"}

        except Exception as e:
            logger.error(f"PayTM verification error: {str(e)}")
            return {"success": False, "error": str(e)}

    def verify_callback(self, response_params, expected_order_id):
        """Verify callback from PayTM redirect"""
        try:
            # Extract checksum
            received_checksum = response_params.get("CHECKSUMHASH", "")

            # Remove checksum from params for verification
            params_copy = response_params.copy()
            params_copy.pop("CHECKSUMHASH", None)

            # Generate checksum
            calculated_checksum = self.generate_checksum(params_copy)

            if received_checksum != calculated_checksum:
                return {"success": False, "error": "Invalid checksum"}

            status = response_params.get("STATUS", "")
            order_id = response_params.get("ORDERID", "")

            if order_id != expected_order_id:
                return {"success": False, "error": "Order ID mismatch"}

            if status == "TXN_SUCCESS":
                return {
                    "success": True,
                    "status": status,
                    "transaction_id": response_params.get("TXNID"),
                    "bank_txn_id": response_params.get("BANKTXNID"),
                    "amount": response_params.get("TXNAMOUNT"),
                }
            else:
                return {
                    "success": False,
                    "status": status,
                    "error": f"Payment status: {status}",
                }

        except Exception as e:
            logger.error(f"PayTM callback verification error: {str(e)}")
            return {"success": False, "error": str(e)}

    def verify_webhook_signature(self, response_params):
        """Verify webhook signature"""
        try:
            received_checksum = response_params.get("CHECKSUMHASH", "")
            params_copy = response_params.copy()
            params_copy.pop("CHECKSUMHASH", None)

            calculated_checksum = self.generate_checksum(params_copy)
            return received_checksum == calculated_checksum

        except Exception as e:
            logger.error(f"Webhook signature verification error: {str(e)}")
            return False


# Create singleton instance
paytm_gateway = PayTMGateway()
