from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import PaymentTransaction, UnlockedExam, UnlockedMockTest


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "order_id_short",
        "user_link",
        "item_name",
        "amount",
        "status_badge",
        "created_at",
        "paid_at",
    ]

    list_filter = ["status", "item_type", "created_at"]
    search_fields = [
        "order_id",
        "user__email",
        "merchant_transaction_id",
        "phonepe_transaction_id",
    ]
    readonly_fields = ["order_id", "created_at", "updated_at", "paid_at"]

    fieldsets = (
        (
            "Transaction Information",
            {
                "fields": (
                    "order_id",
                    "merchant_transaction_id",
                    "phonepe_transaction_id",
                    "phonepe_payment_id",
                )
            },
        ),
        (
            "User & Item",
            {"fields": ("user_link", "item_type", "exam_link", "mock_test_link")},
        ),
        (
            "Payment Details",
            {"fields": ("amount", "status_badge", "created_at", "paid_at")},
        ),
        (
            "Webhook Information",
            {
                "fields": ("webhook_received", "webhook_verified"),
                "classes": ("collapse",),
            },
        ),
        ("Admin Notes", {"fields": ("admin_notes",), "classes": ("collapse",)}),
    )

    actions = ["mark_as_success", "mark_as_failed", "manual_unlock_selected"]

    def order_id_short(self, obj):
        return obj.order_id[:13] + "..." if len(obj.order_id) > 13 else obj.order_id

    order_id_short.short_description = "Order ID"

    def user_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)

    user_link.short_description = "User"

    def exam_link(self, obj):
        if obj.exam:
            url = reverse("admin:exams_exam_change", args=[obj.exam.id])
            return format_html('<a href="{}">{}</a>', url, obj.exam.name)
        return "-"

    exam_link.short_description = "Exam"

    def mock_test_link(self, obj):
        if obj.mock_test:
            url = reverse("admin:mocktests_mocktest_change", args=[obj.mock_test.id])
            return format_html('<a href="{}">{}</a>', url, obj.mock_test.name)
        return "-"

    mock_test_link.short_description = "Mock Test"

    def item_name(self, obj):
        return obj.get_item_name()

    item_name.short_description = "Item"

    def status_badge(self, obj):
        colors = {
            "pending": "gray",
            "processing": "yellow",
            "success": "green",
            "failed": "red",
            "refunded": "orange",
        }
        color = colors.get(obj.status, "gray")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            {
                "gray": "#6b7280",
                "yellow": "#eab308",
                "green": "#10b981",
                "red": "#ef4444",
                "orange": "#f97316",
            }[color],
            obj.status.upper(),
        )

    status_badge.short_description = "Status"

    def mark_as_success(self, request, queryset):
        for transaction in queryset:
            if transaction.status != "success":
                transaction.mark_success()
        self.message_user(
            request, f"{queryset.count()} transaction(s) marked as success."
        )

    mark_as_success.short_description = "Mark selected as success"

    def mark_as_failed(self, request, queryset):
        for transaction in queryset:
            transaction.mark_failed()
        self.message_user(
            request, f"{queryset.count()} transaction(s) marked as failed."
        )

    mark_as_failed.short_description = "Mark selected as failed"

    def manual_unlock_selected(self, request, queryset):
        count = 0
        for transaction in queryset:
            if transaction.status != "success":
                if transaction.exam:
                    UnlockedExam.objects.get_or_create(
                        user=transaction.user, exam=transaction.exam
                    )
                elif transaction.mock_test:
                    UnlockedMockTest.objects.get_or_create(
                        user=transaction.user, mock_test=transaction.mock_test
                    )
                transaction.status = "success"
                transaction.save()
                count += 1
        self.message_user(request, f"{count} transaction(s) manually unlocked.")

    manual_unlock_selected.short_description = "Manual unlock selected (force unlock)"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(UnlockedExam)
class UnlockedExamAdmin(admin.ModelAdmin):
    list_display = ["id", "user_link", "exam_link", "unlocked_at"]
    list_filter = ["unlocked_at"]
    search_fields = ["user__email", "exam__name"]
    readonly_fields = ["unlocked_at"]

    def user_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)

    user_link.short_description = "User"

    def exam_link(self, obj):
        url = reverse("admin:exams_exam_change", args=[obj.exam.id])
        return format_html('<a href="{}">{}</a>', url, obj.exam.name)

    exam_link.short_description = "Exam"

    actions = ["revoke_access"]

    def revoke_access(self, request, queryset):
        count = queryset.delete()[0]
        self.message_user(request, f"{count} unlocked exam(s) revoked.")

    revoke_access.short_description = "Revoke access for selected"

    def has_add_permission(self, request):
        return request.user.is_superuser


@admin.register(UnlockedMockTest)
class UnlockedMockTestAdmin(admin.ModelAdmin):
    list_display = ["id", "user_link", "mock_test_link", "unlocked_at"]
    list_filter = ["unlocked_at"]
    search_fields = ["user__email", "mock_test__name"]
    readonly_fields = ["unlocked_at"]

    def user_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)

    user_link.short_description = "User"

    def mock_test_link(self, obj):
        url = reverse("admin:mocktests_mocktest_change", args=[obj.mock_test.id])
        return format_html('<a href="{}">{}</a>', url, obj.mock_test.name)

    mock_test_link.short_description = "Mock Test"

    actions = ["revoke_access"]

    def revoke_access(self, request, queryset):
        count = queryset.delete()[0]
        self.message_user(request, f"{count} unlocked mock test(s) revoked.")

    revoke_access.short_description = "Revoke access for selected"

    def has_add_permission(self, request):
        return request.user.is_superuser


# Admin site customization
admin.site.site_header = "GovtExamWala Administration"
admin.site.site_title = "GovtExamWala Admin"
admin.site.index_title = "Welcome to GovtExamWala Dashboard"
