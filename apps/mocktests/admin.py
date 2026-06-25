from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Avg, Count
from .models import MockTest, MockTestQuestion, TestAttempt, TestAnswer


class MockTestQuestionInline(admin.TabularInline):
    model = MockTestQuestion
    extra = 1
    fields = ["question", "marks", "order"]
    raw_id_fields = ["question"]


@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "exam",
        "test_type",
        "duration_minutes",
        "total_questions",
        "total_marks",
        "pricing_display",
        "is_active",
        "order",
    ]
    list_filter = ["exam", "test_type", "is_paid", "is_active", "created_at"]
    search_fields = ["name", "description", "exam__name"]
    list_editable = ["order", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [MockTestQuestionInline]
    actions = ["activate_tests", "deactivate_tests", "mark_as_free", "mark_as_paid"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("exam", "subject", "topic", "name", "slug", "test_type")},
        ),
        (
            "Description",
            {"fields": ("description", "instructions"), "classes": ("wide",)},
        ),
        (
            "Test Settings",
            {
                "fields": (
                    "duration_minutes",
                    "total_questions",
                    "total_marks",
                    "passing_marks",
                )
            },
        ),
        (
            "Marking Scheme",
            {
                "fields": (
                    "negative_marking",
                    "negative_mark_value",
                    "marks_per_question",
                )
            },
        ),
        ("Pricing & Availability", {"fields": ("is_paid", "price")}),
        (
            "Display Settings",
            {"fields": ("shuffle_questions", "shuffle_options", "attempts_allowed")},
        ),
        ("Status", {"fields": ("is_active", "order")}),
    )

    def pricing_display(self, obj):
        if obj.is_paid:
            return format_html(
                '<span style="background-color: #fef3c7; color: #d97706; padding: 2px 8px; border-radius: 12px;">💰 Paid - ₹{}</span>',
                obj.price,
            )
        return format_html(
            '<span style="background-color: #d1fae5; color: #059669; padding: 2px 8px; border-radius: 12px;">🎁 Free</span>'
        )

    pricing_display.short_description = "Pricing"

    def activate_tests(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} tests activated.")

    def deactivate_tests(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} tests deactivated.")

    def mark_as_free(self, request, queryset):
        updated = queryset.update(is_paid=False, price=0)
        self.message_user(request, f"{updated} test(s) marked as FREE.")

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(is_paid=True)
        self.message_user(request, f"{updated} test(s) marked as PAID.")


@admin.register(MockTestQuestion)
class MockTestQuestionAdmin(admin.ModelAdmin):
    list_display = ["mock_test_link", "question_preview", "marks", "order"]
    list_filter = ["mock_test__exam", "mock_test"]
    search_fields = ["question__question_text", "mock_test__name"]
    list_editable = ["marks", "order"]
    raw_id_fields = ["question"]

    def mock_test_link(self, obj):
        url = reverse("admin:mocktests_mocktest_change", args=[obj.mock_test.id])
        return format_html('<a href="{}">{}</a>', url, obj.mock_test.name)

    def question_preview(self, obj):
        return (
            obj.question.question_text[:80] + "..."
            if len(obj.question.question_text) > 80
            else obj.question.question_text
        )


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = [
        "user_link",
        "mock_test_link",
        "status_badge",
        "raw_score",
        "percentage",
        "correct_answers",
        "wrong_answers",
        "created_at",
    ]
    list_filter = ["status", "mock_test", "created_at"]
    search_fields = ["user__email", "user__username", "mock_test__name"]
    readonly_fields = [
        "start_time",
        "end_time",
        "total_time_taken",
        "score",
        "percentage",
    ]

    def user_link(self, obj):
        if obj.user:
            url = reverse("admin:accounts_user_change", args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.email)
        guest_id = obj.session_id[:8] if obj.session_id else "Guest"
        return f"Guest ({guest_id})"

    user_link.short_description = "User"

    def mock_test_link(self, obj):
        url = reverse("admin:mocktests_mocktest_change", args=[obj.mock_test.id])
        return format_html('<a href="{}">{}</a>', url, obj.mock_test.name)

    def status_badge(self, obj):
        colors = {
            "in_progress": "#f59e0b",
            "completed": "#10b981",
            "expired": "#ef4444",
        }
        color = colors.get(obj.status, "#6b7280")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.status.replace("_", " ").title(),
        )

    def raw_score(self, obj):
        """Simple score display without formatting - NO float formatting"""
        return f"{obj.score} / {obj.mock_test.total_marks}"

    raw_score.short_description = "Score"


@admin.register(TestAnswer)
class TestAnswerAdmin(admin.ModelAdmin):
    list_display = [
        "attempt_link",
        "question_preview",
        "selected_option",
        "is_correct_badge",
        "marks_obtained",
        "time_taken",
    ]
    list_filter = ["is_correct", "is_skipped"]
    search_fields = ["question__question_text", "attempt__user__email"]
    list_editable = ["marks_obtained"]

    def attempt_link(self, obj):
        url = reverse("admin:mocktests_testattempt_change", args=[obj.attempt.id])
        if obj.attempt.user:
            return format_html(
                '<a href="{}">{} - Attempt #{}</a>',
                url,
                obj.attempt.user.email,
                obj.attempt.id,
            )
        guest_id = obj.attempt.session_id[:8] if obj.attempt.session_id else "Guest"
        return format_html(
            '<a href="{}">Guest ({}) - Attempt #{}</a>', url, guest_id, obj.attempt.id
        )

    def question_preview(self, obj):
        return (
            obj.question.question_text[:60] + "..."
            if len(obj.question.question_text) > 60
            else obj.question.question_text
        )

    def is_correct_badge(self, obj):
        if obj.is_correct:
            return format_html('<span style="color: #10b981;">✓ Correct</span>')
        elif obj.is_skipped:
            return format_html('<span style="color: #6b7280;">⊘ Skipped</span>')
        return format_html('<span style="color: #ef4444;">✗ Wrong</span>')
