import json
import base64
import hashlib
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from django.conf import settings


class PhonePeGateway:
    """PhonePe Payment Gateway Integration"""

    def __init__(self):
        self.merchant_id = settings.PHONEPE_MERCHANT_ID
        self.salt_key = settings.PHONEPE_SALT_KEY
        self.salt_index = settings.PHONEPE_SALT_INDEX
        self.base_url = settings.PHONEPE_BASE_URL

    def generate_payload(self, order_id, amount, user_id, user_email, redirect_url):
        """Generate payment payload for PhonePe"""

        # Create merchant transaction ID
        merchant_transaction_id = f"{self.merchant_id}_{order_id}"

        payload = {
            "merchantId": self.merchant_id,
            "merchantTransactionId": merchant_transaction_id,
            "merchantUserId": str(user_id),
            "amount": int(amount * 100),  # Convert to paise
            "redirectUrl": redirect_url,
            "redirectMode": "REDIRECT",
            "callbackUrl": f"{settings.BASE_URL}/payments/webhook/phonepe/",
            "mobileNumber": "",
            "paymentInstrument": {"type": "PAY_PAGE"},
        }

        return payload, merchant_transaction_id

    def generate_qr_payload(self, order_id, amount, user_id):
        """Generate payload for QR code payment"""

        merchant_transaction_id = f"{self.merchant_id}_{order_id}"

        payload = {
            "merchantId": self.merchant_id,
            "merchantTransactionId": merchant_transaction_id,
            "merchantUserId": str(user_id),
            "amount": int(amount * 100),
            "callbackUrl": f"{settings.BASE_URL}/payments/webhook/phonepe/",
            "paymentInstrument": {"type": "QR_CODE"},
        }

        return payload, merchant_transaction_id

    def encode_payload(self, payload):
        """Encode payload to base64"""
        payload_json = json.dumps(payload)
        payload_base64 = base64.b64encode(payload_json.encode()).decode()
        return payload_base64

    def generate_checksum(self, payload_base64):
        """Generate SHA256 checksum for verification"""
        checksum_string = f"{payload_base64}/pg/v1/pay{self.salt_key}"
        checksum = hashlib.sha256(checksum_string.encode()).hexdigest()
        return f"{checksum}###{self.salt_index}"

    def create_payment_request(
        self, order_id, amount, user_id, user_email, redirect_url
    ):
        """Create payment request and get payment URL"""

        payload, merchant_transaction_id = self.generate_payload(
            order_id, amount, user_id, user_email, redirect_url
        )

        payload_base64 = self.encode_payload(payload)
        checksum = self.generate_checksum(payload_base64)

        headers = {"Content-Type": "application/json", "X-VERIFY": checksum}

        request_body = {"request": payload_base64}

        try:
            response = requests.post(
                f"{self.base_url}/pg/v1/pay", json=request_body, headers=headers
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return {
                        "success": True,
                        "payment_url": data["data"]["instrumentResponse"][
                            "redirectInfo"
                        ]["url"],
                        "merchant_transaction_id": merchant_transaction_id,
                    }
                else:
                    return {
                        "success": False,
                        "error": data.get("message", "Payment initiation failed"),
                    }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_qr_payment(self, order_id, amount, user_id):
        """Create QR code for payment"""

        payload, merchant_transaction_id = self.generate_qr_payload(
            order_id, amount, user_id
        )

        payload_base64 = self.encode_payload(payload)
        checksum = self.generate_checksum(payload_base64)

        headers = {"Content-Type": "application/json", "X-VERIFY": checksum}

        request_body = {"request": payload_base64}

        try:
            response = requests.post(
                f"{self.base_url}/pg/v1/pay", json=request_body, headers=headers
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return {
                        "success": True,
                        "qr_code_url": data["data"].get("qrCodeUrl"),
                        "qr_code_base64": data["data"].get("qrCode"),
                        "merchant_transaction_id": merchant_transaction_id,
                    }
                else:
                    return {
                        "success": False,
                        "error": data.get("message", "QR generation failed"),
                    }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def verify_payment(self, merchant_transaction_id):
        """Verify payment status with PhonePe"""

        # Create checksum for verification
        checksum_string = (
            f"/pg/v1/status/{self.merchant_id}/{merchant_transaction_id}{self.salt_key}"
        )
        checksum = hashlib.sha256(checksum_string.encode()).hexdigest()
        checksum = f"{checksum}###{self.salt_index}"

        headers = {
            "Content-Type": "application/json",
            "X-VERIFY": checksum,
            "X-MERCHANT-ID": self.merchant_id,
        }

        try:
            response = requests.get(
                f"{self.base_url}/pg/v1/status/{self.merchant_id}/{merchant_transaction_id}",
                headers=headers,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    payment_data = data.get("data", {})
                    return {
                        "success": True,
                        "status": payment_data.get("state"),
                        "amount": payment_data.get("amount"),
                        "transaction_id": payment_data.get("transactionId"),
                        "payment_instrument": payment_data.get("paymentInstrument"),
                    }
                else:
                    return {
                        "success": False,
                        "error": data.get("message", "Verification failed"),
                    }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def decode_callback_response(self, encrypted_response):
        """Decrypt webhook callback response"""
        try:
            # Decode base64
            encrypted_data = base64.b64decode(encrypted_response)

            # Extract IV and encrypted data
            iv = encrypted_data[:16]
            ciphertext = encrypted_data[16:]

            # Create cipher
            cipher = AES.new(self.salt_key.encode()[:32], AES.MODE_CBC, iv)

            # Decrypt and unpad
            decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

            return json.loads(decrypted.decode())
        except Exception as e:
            return None


# Initialize PhonePe gateway
phonepe_gateway = PhonePeGateway()
