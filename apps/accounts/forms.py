from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from .models import User


class UserRegistrationForm(forms.ModelForm):
    """Form for traditional password-based registration"""

    # username = forms.CharField(
    #     required=True,
    #     widget=forms.TextInput(attrs={
    #         'placeholder': 'Choose a username',
    #         'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500'
    #     })
    # )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your email",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500",
            }
        ),
        error_messages={
            "invalid": "Please enter a valid email address",
            "required": "Email address is required",
        },
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Create a password",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm your password",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500",
            }
        ),
    )

    class Meta:
        model = User
        # fields = ['username', 'email', 'password1', 'password2']
        fields = ["email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered. Please login.")
        return email

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('Username already taken. Please choose another.')
    #     if len(username) < 3:
    #         raise forms.ValidationError('Username must be at least 3 characters')
    #     return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_verified = True
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """Form for traditional password-based login"""

    login_input = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500",
            }
        ),
        error_messages={"required": "Email is required"},
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500",
            }
        ),
        error_messages={"required": "Password is required"},
    )
    remember = forms.BooleanField(required=False)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your registered email",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500",
            }
        ),
    )


class VerifyOTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter 6-digit OTP",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-center text-2xl tracking-widest",
            }
        ),
    )

    def clean_otp(self):
        otp = self.cleaned_data.get("otp")
        if otp and not otp.isdigit():
            raise forms.ValidationError("OTP must contain only numbers")
        if otp and len(otp) != 6:
            raise forms.ValidationError("OTP must be exactly 6 digits")
        return otp


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New password",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg",
            }
        ),
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm new password",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = ['username', 'first_name', 'last_name', 'profile_pic']
        fields = ["first_name", "last_name", "profile_pic"]


# Add these forms to your existing forms.py


class SetPasswordForm(forms.Form):
    """Form for setting password after OTP signup"""

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter new password",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500",
            }
        ),
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm password",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        if password and len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long")

        return cleaned_data


class ChangePasswordForm(forms.Form):
    """Form for changing existing password"""

    current_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter current password",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500",
            }
        ),
    )
    new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter new password",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500",
            }
        ),
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm new password",
                "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match")

        if new_password and len(new_password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long")

        return cleaned_data
