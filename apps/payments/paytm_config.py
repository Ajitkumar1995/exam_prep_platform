import hashlib
import json
import requests
from django.conf import settings


class PayTMConfig:
    """PayTM Payment Gateway Configuration for Staging/Test"""

    # Staging/Test Environment URLs
    STAGING_URL = "https://securegw-stage.paytm.in"
    PRODUCTION_URL = "https://securegw.paytm.in"

    # API Endpoints
    PAYMENT_INITIATE_URL = "/theia/api/v1/initiateTransaction"
    TRANSACTION_STATUS_URL = "/merchant-status/api/v1/getPaymentStatus"
    REFUND_URL = "/v2/refund"

    # Test Credentials (Staging)
    MERCHANT_ID = "YOUR_TEST_MERCHANT_ID"  # Get from PayTM dashboard
    MERCHANT_KEY = "YOUR_TEST_MERCHANT_KEY"  # Get from PayTM dashboard

    # Configuration
    INDUSTRY_TYPE_ID = "Retail"
    CHANNEL_ID = "WEB"  # WEB for website, WAP for mobile
    WEBSITE = "WEBSTAGING"  # For staging
    CALLBACK_URL = None  # Set dynamically

    @staticmethod
    def get_base_url():
        """Get base URL based on environment"""
        if getattr(settings, "PAYTM_DEBUG", True):
            return PayTMConfig.STAGING_URL
        return PayTMConfig.PRODUCTION_URL

    @staticmethod
    def generate_checksum(params, merchant_key):
        """Generate checksum hash for PayTM"""
        # Sort parameters alphabetically
        sorted_params = sorted(params.items())

        # Create parameter string
        param_string = ""
        for key, value in sorted_params:
            if value is not None and value != "":
                param_string += f"{key}={value}&"

        # Remove trailing &
        param_string = param_string.rstrip("&")

        # Generate checksum
        checksum = hashlib.sha256((param_string + merchant_key).encode()).hexdigest()

        return checksum

    @staticmethod
    def verify_checksum(response_params, merchant_key):
        """Verify PayTM response checksum"""
        # Extract checksum from response
        received_checksum = response_params.get("CHECKSUMHASH", "")

        # Remove checksum from parameters for verification
        response_params_copy = response_params.copy()
        response_params_copy.pop("CHECKSUMHASH", None)

        # Generate checksum
        calculated_checksum = PayTMConfig.generate_checksum(
            response_params_copy, merchant_key
        )

        return received_checksum == calculated_checksum

    @staticmethod
    def get_test_credentials():
        """Get PayTM test credentials"""
        return {
            "mobile": "7777777777",
            "otp": "489871",
            "password": "Paytm12345",
            "card_number": "4111111111111111",
            "expiry": "12/25",
            "cvv": "123",
        }
