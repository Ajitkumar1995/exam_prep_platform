from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # Main auth page
    path("auth/", views.login_signup, name="login_signup"),
    # Traditional password-based auth
    path("password-login/", views.password_login, name="password_login"),
    path("password-register/", views.password_register, name="password_register"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path(
        "reset-password/<uidb64>/<token>/",
        views.password_reset_confirm,
        name="password_reset_confirm",
    ),
    # OTP-based auth (existing)
    path("otp-send/", views.otp_send, name="otp_send"),
    path("verify-otp/", views.verify_otp_from_email, name="verify_otp_from_email"),
    # Password management
    path("set-password/", views.set_password, name="set_password"),
    path("change-password/", views.change_password, name="change_password"),
    # Common
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    # API
    path("api/check-email/", views.check_email_exists, name="check_email"),
    path("api/check-username/", views.check_username_exists, name="check_username"),
]
