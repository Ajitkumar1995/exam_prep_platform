from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import User, OTP


class CustomUserAdmin(UserAdmin):
    list_display = ["id", "email", "is_verified", "is_active", "date_joined"]
    list_filter = ["is_verified", "is_active", "date_joined"]
    search_fields = ["email"]
    ordering = ["-date_joined"]

    fieldsets = (
        ("User Information", {"fields": ("email", "profile_pic")}),
        ("Status", {"fields": ("is_verified", "is_active")}),
        (
            "Important Dates",
            {"fields": ("last_login", "date_joined"), "classes": ("collapse",)},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email",),
            },
        ),
    )

    readonly_fields = ["date_joined", "last_login"]

    actions = ["verify_users"]

    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f"{queryset.count()} user(s) verified successfully.")

    verify_users.short_description = "Verify selected users"


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ["id", "user_link", "otp", "is_used", "created_at", "expires_at"]
    list_filter = ["is_used", "created_at"]
    search_fields = ["user__email", "otp"]
    readonly_fields = ["created_at"]

    def user_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)

    user_link.short_description = "User"

    def has_add_permission(self, request):
        return False


admin.site.register(User, CustomUserAdmin)
admin.site.site_header = "GovtExamWala Administration"
admin.site.site_title = "GovtExamWala Admin Portal"
admin.site.index_title = "Welcome to GovtExamWala Admin Dashboard"
