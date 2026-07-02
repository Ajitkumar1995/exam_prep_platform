from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from .models import User, OTP
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    ForgotPasswordForm,
    VerifyOTPForm,
    ResetPasswordForm,
    ProfileUpdateForm,
    SetPasswordForm,
    ChangePasswordForm,
)
from .utils import create_otp, verify_otp
from .tasks import send_email_task
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import views as auth_views
import logging

logger = logging.getLogger(__name__)


def login_signup(request):
    """Combined login and signup page with both OTP and Password options"""
    login_form = UserLoginForm()
    signup_form = UserRegistrationForm()
    return render(
        request,
        "accounts/login_signup.html",
        {"login_form": login_form, "signup_form": signup_form},
    )


# ==================== PASSWORD-BASED AUTHENTICATION ====================


def password_login(request):
    """Traditional login with email/username and password"""
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data["login_input"]
            password = form.cleaned_data["password"]
            remember = form.cleaned_data.get("remember", False)

            # Check if input is email
            if "@" in login_input:
                # It's an email
                try:
                    user = User.objects.get(email=login_input)
                except User.DoesNotExist:
                    messages.error(request, "Invalid email or password.")
                    return redirect("accounts:login_signup")
            else:
                # It's a username
                try:
                    user = User.objects.get(username=login_input)
                except User.DoesNotExist:
                    messages.error(request, "Invalid username or password.")
                    return redirect("accounts:login_signup")

            # Authenticate user
            user = authenticate(request, username=user.email, password=password)

            if user is not None:
                login(request, user)

                if not remember:
                    request.session.set_expiry(0)

                messages.success(request, f"Welcome back, {user.username}!")

                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect("accounts:dashboard")
            else:
                messages.error(request, "Invalid email/username or password.")
        else:
            for error in form.errors.values():
                messages.error(request, error)

    return redirect("accounts:login_signup")


def password_register(request):
    """Traditional registration with email, username, and password"""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = (
                True  # Password-based registration doesn't need email verification
            )
            user.save()

            # Log the user in
            login(request, user)

            messages.success(
                request, f"Account created successfully! Welcome {user.username}!"
            )
            return redirect("accounts:dashboard")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return redirect("accounts:login_signup")


# ==================== OTP-BASED AUTHENTICATION (Existing) ====================


def otp_send(request):
    """Send OTP for login/signup (existing functionality)"""
    if request.method == "POST":
        email = request.POST.get("email")
        purpose = request.POST.get("purpose", "signup")

        if not email:
            messages.error(request, "Email is required...")
            return redirect("accounts:login_signup")

        # Check if user exists
        user_exists = User.objects.filter(email=email).exists()

        if purpose == "signup":
            if user_exists:
                messages.error(
                    request, "Email already registered. Please login instead."
                )
                return redirect("accounts:login_signup")
            # Create new user (pending verification)
            user = User.objects.create_user(
                email=email, username=email, is_active=True, is_verified=False
            )
            # IMPORTANT: Make sure no password is set
            user.set_unusable_password()  # ADD THIS LINE
            user.save()
        else:  # login
            if not user_exists:
                messages.error(
                    request, "No account found with this email. Please sign up first."
                )
                return redirect("accounts:login_signup")

            user = User.objects.get(email=email)

        # Create and send OTP
        create_otp(user, purpose)

        # Store in session
        request.session["otp_user_id"] = user.id
        request.session["otp_email"] = email
        request.session["otp_purpose"] = purpose

        messages.success(request, f"OTP sent to {email}. Please verify to continue.")
        # return redirect('accounts:verify_otp')
        return redirect("accounts:verify_otp_from_email")

    return redirect("accounts:login_signup")


def verify_otp_from_email(request):
    """Verify OTP and complete login/signup (existing functionality)"""
    user_id = request.session.get("otp_user_id")
    email = request.session.get("otp_email")
    purpose = request.session.get("otp_purpose")

    if not user_id or not email:
        messages.error(request, "Session expired. Please try again.")
        return redirect("accounts:login_signup")

    user = get_object_or_404(User, id=user_id, email=email)

    if request.method == "POST":
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data["otp"]

            # if verify_otp(user, otp_code):
            if verify_otp(user, otp_code, purpose):
                if purpose == "signup":
                    user.is_verified = True
                    user.save()
                    messages.success(
                        request,
                        "Account created successfully! Welcome to GovtExamWala.",
                    )
                else:
                    messages.success(request, f"Welcome back, {email}!")

                login(request, user)

                # Clear session
                del request.session["otp_user_id"]
                del request.session["otp_email"]
                del request.session["otp_purpose"]

                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect("accounts:dashboard")
            else:
                messages.error(request, "Invalid or expired OTP. Please try again.")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = VerifyOTPForm()

    # Handle resend
    if request.GET.get("resend"):
        create_otp(user, purpose)
        messages.success(request, f"New OTP sent to {email}")
        return redirect("accounts:verify_otp_from_email")

    return render(
        request,
        "accounts/verify_otp.html",
        {"form": form, "email": email, "purpose": purpose},
    )


def forgot_password(request):
    """Handle forgot password request - sends reset link via email"""
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email, is_active=True)

            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Build reset link
            reset_url = request.build_absolute_uri(
                reverse(
                    "accounts:password_reset_confirm",
                    kwargs={"uidb64": uid, "token": token},
                )
            )

            # Email subject and body
            subject = "Password Reset Request - GovtExamWala"
            message = f"""
                    Hello {user.username},

                    You requested a password reset for your GovtExamWala account.

                    Click the link below to reset your password:

                    {reset_url}

                    This link will expire in 10 Minutes.

                    If you didn't request this password reset, please ignore this email.

                    Best regards,
                    GovtExamWala Team
                    """

            try:
                send_email_task.delay(
                    subject,
                    message,
                    [email],
                    "GovtExamWala <noreply@govtexamwala.com>",
                )
                logger.info("Password reset email queued for %s", email)
                messages.success(
                    request,
                    f"Password reset link has been sent to {email}. Please check your inbox.",
                )
                return redirect("accounts:login_signup")
            except Exception as e:
                logger.warning(
                    "Celery unavailable for password reset email to %s: %s",
                    email,
                    e,
                )
                try:
                    send_email_task.apply(
                        args=[
                            subject,
                            message,
                            [email],
                            "GovtExamWala <noreply@govtexamwala.com>",
                        ]
                    )
                    messages.success(
                        request,
                        f"Password reset link has been sent to {email}. Please check your inbox.",
                    )
                    return redirect("accounts:login_signup")
                except Exception as fallback_error:
                    logger.error(
                        "Failed to send password reset email to %s: %s",
                        email,
                        fallback_error,
                    )
                    messages.error(
                        request, "Unable to send reset link. Please try again later."
                    )
                    return redirect("accounts:forgot_password")

        except User.DoesNotExist:
            # For security, don't reveal if email exists or not
            messages.success(
                request,
                f"If an account exists with {email}, a password reset link has been sent.",
            )
            logger.warning(f"Password reset requested for non-existent email: {email}")
            return redirect("accounts:login_signup")

    return render(request, "accounts/forgot_password.html")


def password_reset_confirm(request, uidb64, token):
    """Confirm password reset and set new password"""
    try:
        # Decode user ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Valid token
        if request.method == "POST":
            password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if not password:
                messages.error(request, "Password is required.")
                return redirect(
                    "accounts:password_reset_confirm", uidb64=uidb64, token=token
                )

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect(
                    "accounts:password_reset_confirm", uidb64=uidb64, token=token
                )

            if len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
                return redirect(
                    "accounts:password_reset_confirm", uidb64=uidb64, token=token
                )

            # Set new password
            user.set_password(password)
            user.save()

            messages.success(
                request,
                "Password has been reset successfully! You can now login with your new password.",
            )
            return redirect("accounts:login_signup")

        return render(
            request,
            "accounts/password_reset_form.html",
            {"uidb64": uidb64, "token": token},
        )
    else:
        # Invalid or expired token
        messages.error(
            request,
            "The password reset link is invalid or has expired. Please request a new one.",
        )
        return redirect("accounts:forgot_password")


def user_logout(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")


@login_required
def dashboard(request):
    """User dashboard after login"""
    from apps.mocktests.models import TestAttempt
    from django.db import models

    stats = TestAttempt.objects.filter(user=request.user, status="completed").aggregate(
        total_tests=models.Count("id"),
        avg_score=models.Avg("percentage"),
    )
    recent_tests = TestAttempt.objects.filter(
        user=request.user, status="completed"
    ).select_related("mock_test", "mock_test__exam").order_by("-end_time")[:5]

    context = {
        "total_tests": stats["total_tests"] or 0,
        "avg_score": round(stats["avg_score"] or 0, 1),
        "recent_tests": recent_tests,
        "user": request.user,
    }
    return render(request, "accounts/dashboard.html", context)


@login_required
def profile(request):
    """User profile page"""
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(
        request, "accounts/profile.html", {"form": form, "user": request.user}
    )


# ==================== API VIEWS ====================


def check_email_exists(request):
    """Check if email already exists (AJAX)"""
    email = request.GET.get("email")
    if email:
        exists = User.objects.filter(email=email).exists()
        return JsonResponse({"exists": exists})
    return JsonResponse({"error": "No email provided"}, status=400)


def check_username_exists(request):
    """Check if username already exists (AJAX)"""
    username = request.GET.get("username")
    if username:
        exists = User.objects.filter(username=username).exists()
        return JsonResponse({"exists": exists})
    return JsonResponse({"error": "No username provided"}, status=400)


# ==================== PASSWORD MANAGEMENT ====================


@login_required
def set_password(request):
    """Allow OTP users to set a password for their account"""
    # If user already has a password, redirect to change password
    if request.user.has_usable_password():
        messages.info(
            request, "You already have a password. You can change it instead."
        )
        return redirect("accounts:change_password")

    if request.method == "POST":
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            request.user.set_password(password)
            request.user.save()

            # Re-authenticate the user
            user = authenticate(request, username=request.user.email, password=password)
            if user:
                login(request, user)

            messages.success(
                request,
                "Password set successfully! You can now login using email and password.",
            )
            return redirect("accounts:profile")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = SetPasswordForm()

    return render(
        request, "accounts/set_password.html", {"form": form, "user": request.user}
    )


@login_required
def change_password(request):
    """Allow users to change their existing password"""
    # If user doesn't have a password, redirect to set password
    if not request.user.has_usable_password():
        messages.info(request, "Please set a password first.")
        return redirect("accounts:set_password")

    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data["current_password"]
            new_password = form.cleaned_data["new_password"]

            # Verify current password
            if not request.user.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
                return redirect("accounts:change_password")

            # Set new password
            request.user.set_password(new_password)
            request.user.save()

            # Update session to prevent logout
            update_session_auth_hash(request, request.user)

            messages.success(request, "Password changed successfully!")
            return redirect("accounts:profile")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ChangePasswordForm()

    return render(
        request, "accounts/change_password.html", {"form": form, "user": request.user}
    )
