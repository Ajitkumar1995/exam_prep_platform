import json
import uuid
import requests
from decimal import Decimal
from django.utils import timezone
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .paytm_config import PayTMConfig
from .models import PaymentTransaction, UnlockedExam, UnlockedMockTest


class PayTMPaymentService:
    """PayTM Payment Service Handler"""

    @staticmethod
    def initiate_payment(request, user, item_type, item_id, amount, order_id):
        """
        Initiate PayTM payment
        Returns HTML form for auto-submission
        """
        from apps.exams.models import Exam
        from apps.mocktests.models import MockTest

        # Get the item
        if item_type == "exam":
            item = Exam.objects.filter(id=item_id, is_active=True).first()
            if not item:
                return None, "Exam not found"
        else:
            item = MockTest.objects.filter(id=item_id, is_active=True).first()
            if not item:
                return None, "Mock test not found"

        # Create transaction record
        transaction = PaymentTransaction.objects.create(
            user=user,
            item_type=item_type,
            exam=item if item_type == "exam" else None,
            mock_test=item if item_type == "mock_test" else None,
            amount=amount,
            status="processing",
            order_id=order_id,
        )

        # Prepare PayTM parameters
        callback_url = request.build_absolute_uri("/payments/paytm-callback/")

        params = {
            "MID": PayTMConfig.MERCHANT_ID,
            "ORDER_ID": order_id,
            "TXN_AMOUNT": str(float(amount)),
            "CUST_ID": str(user.id),
            "INDUSTRY_TYPE_ID": PayTMConfig.INDUSTRY_TYPE_ID,
            "CHANNEL_ID": PayTMConfig.CHANNEL_ID,
            "WEBSITE": PayTMConfig.WEBSITE,
            "CALLBACK_URL": callback_url,
            "EMAIL": user.email,
            "MOBILE_NO": getattr(user, "phone", ""),
        }

        # Generate checksum
        checksum = PayTMConfig.generate_checksum(params, PayTMConfig.MERCHANT_KEY)
        params["CHECKSUMHASH"] = checksum

        # Store transaction details in session
        request.session["paytm_order_id"] = order_id
        request.session["paytm_amount"] = str(amount)

        # Return HTML form for auto-submission
        return params, None

    @staticmethod
    def verify_payment(order_id):
        """
        Verify payment status with PayTM
        """
        # Prepare parameters for status check
        params = {"MID": PayTMConfig.MERCHANT_ID, "ORDER_ID": order_id}

        # Generate checksum
        checksum = PayTMConfig.generate_checksum(params, PayTMConfig.MERCHANT_KEY)

        # Prepare request
        url = f"{PayTMConfig.get_base_url()}{PayTMConfig.TRANSACTION_STATUS_URL}"
        headers = {"Content-Type": "application/json", "X-VERIFY": checksum}

        try:
            response = requests.post(url, json=params, headers=headers, timeout=30)

            if response.status_code == 200:
                response_data = response.json()

                # Verify response checksum
                if PayTMConfig.verify_checksum(response_data, PayTMConfig.MERCHANT_KEY):
                    status = response_data.get("STATUS", "")

                    if status == "TXN_SUCCESS":
                        # Payment successful
                        transaction = PaymentTransaction.objects.filter(
                            order_id=order_id
                        ).first()

                        if transaction:
                            transaction.mark_success(
                                phonepe_transaction_id=response_data.get("TXN_ID"),
                                phonepe_payment_id=response_data.get("BANKTXNID"),
                            )
                            return transaction, "Payment successful"

                    elif status == "PENDING":
                        return None, "Payment pending"
                    else:
                        return None, f"Payment failed: {status}"
                else:
                    return None, "Invalid checksum"
            else:
                return None, f"API Error: {response.status_code}"

        except Exception as e:
            return None, str(e)

    @staticmethod
    def process_callback(request):
        """
        Process PayTM callback response
        """
        response_params = request.POST.dict()

        # Verify checksum
        if not PayTMConfig.verify_checksum(response_params, PayTMConfig.MERCHANT_KEY):
            return None, "Invalid checksum"

        order_id = response_params.get("ORDER_ID")
        status = response_params.get("STATUS")

        if status == "TXN_SUCCESS":
            # Verify payment
            transaction, message = PayTMPaymentService.verify_payment(order_id)
            if transaction:
                return transaction, "Payment successful"

        return None, f"Payment failed: {status}"

    @staticmethod
    def generate_test_form(request, amount=100):
        """
        Generate test payment form for development
        """
        order_id = f"TEST_{uuid.uuid4().hex[:10]}"

        params = {
            "MID": PayTMConfig.MERCHANT_ID,
            "ORDER_ID": order_id,
            "TXN_AMOUNT": str(amount),
            "CUST_ID": "TEST_USER",
            "INDUSTRY_TYPE_ID": PayTMConfig.INDUSTRY_TYPE_ID,
            "CHANNEL_ID": PayTMConfig.CHANNEL_ID,
            "WEBSITE": PayTMConfig.WEBSITE,
            "CALLBACK_URL": request.build_absolute_uri("/payments/paytm-callback/"),
            "EMAIL": "test@example.com",
            "MOBILE_NO": "7777777777",
        }

        # Generate checksum
        checksum = PayTMConfig.generate_checksum(params, PayTMConfig.MERCHANT_KEY)
        params["CHECKSUMHASH"] = checksum

        return params
