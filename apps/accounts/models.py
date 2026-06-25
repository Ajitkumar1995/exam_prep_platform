from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager"""

    def create_user(self, email, password=None, username=None, **extra_fields):
        """Create and save a regular user"""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)

        # If username is not provided, use email as username
        if not username:
            username = email

        # Ensure username is unique
        base_username = username
        counter = 1
        while self.model.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = self.model(email=email, username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, username, **extra_fields)


class User(AbstractUser):
    """
    User model - Admin can set username/password, regular users use email as username
    """

    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="profiles/", null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # Use custom manager
    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # For regular users (non-staff, non-superuser), set username = email if not set
        if not self.is_staff and not self.is_superuser:
            if not self.username or self.username != self.email:
                self.username = self.email
        super().save(*args, **kwargs)


class OTP(models.Model):
    """
    OTP model for email verification
    """

    OTP_TYPES = (
        ("email", "Email Verification"),
        ("phone", "Phone Verification"),
        ("login", "Login OTP"),
        ("signup", "Signup OTP"),
        ("password", "Password Reset"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    otp = models.CharField(max_length=6)
    otp_type = models.CharField(max_length=20, choices=OTP_TYPES, default="email")
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=10)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.otp} - {self.otp_type}"
