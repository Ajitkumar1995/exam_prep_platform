import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


def generate_otp():
    return "".join(random.choices(string.digits, k=6))


def otp_send_email(email, otp, purpose="verification"):
    """Send OTP via email with better formatting to avoid spam"""
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
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,  # Send HTML version
        )
        print(f"OTP email sent successfully to {email}")
        return True
    except Exception as e:
        print(f"Failed to send OTP email to {email}: {str(e)}")
        return False


def create_otp(user, purpose="verification"):
    from .models import OTP

    otp_code = generate_otp()

    # Delete old OTPs for this purpose/type
    OTP.objects.filter(user=user, otp_type=purpose, is_used=False).delete()

    expires_at = timezone.now() + timedelta(minutes=10)

    # Make sure otp_type is set
    otp = OTP.objects.create(
        user=user,
        otp=otp_code,
        otp_type=purpose,  # This should be 'signup' or 'login'
        expires_at=expires_at,
        is_used=False,
    )

    print(f"DEBUG - OTP created: {otp_code} for {user.email} with type {purpose}")

    otp_send_email(user.email, otp_code, purpose)
    return otp


def verify_otp(user, otp_code, otp_type="email"):  # CHANGE THIS - add parameters
    """Verify OTP for user"""
    from .models import OTP

    print(f"DEBUG - Verifying OTP: user={user.email}, otp={otp_code}, type={otp_type}")

    try:
        otp = OTP.objects.get(user=user, otp=otp_code, otp_type=otp_type, is_used=False)

        if otp.is_valid():
            otp.is_used = True
            otp.save()
            print(f"DEBUG - OTP verified successfully")
            return True
        else:
            print(
                f"DEBUG - OTP expired (expires_at: {otp.expires_at}, now: {timezone.now()})"
            )
            return False
    except OTP.DoesNotExist:
        print(
            f"DEBUG - OTP not found for user={user.email}, otp={otp_code}, type={otp_type}"
        )
        return False
