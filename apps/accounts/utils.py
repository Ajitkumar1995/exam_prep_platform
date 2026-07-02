import random
import string
import logging
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from kombu.exceptions import OperationalError

from .tasks import send_email_task

logger = logging.getLogger(__name__)


def generate_otp():
    """Generate a six-digit numeric OTP."""
    return "".join(random.choices(string.digits, k=6))


def otp_send_email(email, otp, purpose="verification"):
    """Queue an OTP email and fall back to synchronous sending if needed."""
    subject = f"Your {purpose} code for GovtExamWala"

    # HTML email format (better for spam filters)
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #4F46E5; color: white; padding: 20px; text-align: center; }}
            .otp {{ font-size: 32px; font-weight: bold; color: #4F46E5; text-align: center; padding: 20px; }}
            .footer {{ font-size: 12px; color: gray; text-align: center; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>GovtExamWala.com</h2>
            </div>
            <div class="otp">
                Your OTP: <strong>{otp}</strong>
            </div>
            <p>This code will expire in 10 minutes.</p>
            <p>If you didn't request this, please ignore this email.</p>
            <div class="footer">
                <p>GovtExamWala - Your Exam Preparation Partner</p>
            </div>
        </div>
    </body>
    </html>
    """

    plain_message = f"""
    Your {purpose} code for GovtExamWala is: {otp}
    
    This code will expire in 10 minutes.
    
    If you didn't request this, please ignore this email.
    
    Best regards,
    GovtExamWala Team
    """

    try:
        send_email_task.delay(
            subject,
            plain_message,
            [email],
            settings.DEFAULT_FROM_EMAIL,
            html_message=html_message,
        )
        logger.info("OTP email queued for %s", email)
        return True
    except OperationalError as exc:
        logger.warning("Celery unavailable for OTP email to %s: %s", email, exc)
        try:
            send_email_task.apply(
                args=[
                    subject,
                    plain_message,
                    [email],
                    settings.DEFAULT_FROM_EMAIL,
                ],
                kwargs={"html_message": html_message},
            )
            return True
        except Exception as fallback_exc:
            logger.warning("Failed to send OTP email to %s: %s", email, fallback_exc)
            return False


def create_otp(user, purpose="verification"):
    """Create a fresh OTP for a user and send it by email."""
    from .models import OTP

    otp_code = generate_otp()

    OTP.objects.filter(user=user, otp_type=purpose, is_used=False).delete()

    expires_at = timezone.now() + timedelta(minutes=10)

    otp = OTP.objects.create(
        user=user,
        otp=otp_code,
        otp_type=purpose,
        expires_at=expires_at,
        is_used=False,
    )

    logger.debug("OTP created for user=%s type=%s", user.email, purpose)

    otp_send_email(user.email, otp_code, purpose)
    return otp


def verify_otp(user, otp_code, otp_type="email"):
    """Validate an unused OTP and mark it as consumed."""
    from .models import OTP

    logger.debug("Verifying OTP for user=%s type=%s", user.email, otp_type)

    try:
        otp = OTP.objects.get(user=user, otp=otp_code, otp_type=otp_type, is_used=False)

        if otp.is_valid():
            otp.is_used = True
            otp.save()
            logger.debug("OTP verified successfully for user=%s", user.email)
            return True
        else:
            logger.debug(
                "OTP expired for user=%s expires_at=%s now=%s",
                user.email,
                otp.expires_at,
                timezone.now(),
            )
            return False
    except OTP.DoesNotExist:
        logger.debug("OTP not found for user=%s type=%s", user.email, otp_type)
        return False
