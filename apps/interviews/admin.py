from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import InterviewCategory, InterviewQuestion, UserInterviewProgress


@admin.register(InterviewCategory)
class InterviewCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "icon", "order", "questions_count", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "description"]
    list_editable = ["order", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "slug", "icon", "description", "order")},
        ),
        ("Status", {"fields": ("is_active",)}),
    )

    def questions_count(self, obj):
        count = obj.questions.filter(is_active=True).count()
        url = (
            reverse("admin:interviews_interviewquestion_changelist")
            + f"?category__id={obj.id}"
        )
        return format_html('<a href="{}">{} Questions</a>', url, count)

    questions_count.short_description = "Questions"


class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = [
        "question_preview",
        "category",
        "question_type",
        "difficulty",
        "time_limit",
        "is_active",
    ]
    list_filter = ["category", "question_type", "difficulty", "is_active"]
    search_fields = ["question_text", "keywords", "tips"]
    list_editable = ["is_active"]
    list_per_page = 20
    save_on_top = True
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("category", "question_type", "difficulty", "question_text")},
        ),
        (
            "Answer & Evaluation",
            {"fields": ("sample_answer", "keywords", "tips"), "classes": ("wide",)},
        ),
        ("Settings", {"fields": ("time_limit", "is_active")}),
    )

    def question_preview(self, obj):
        preview = obj.question_text[:80]
        return format_html(
            '<span title="{}">{}{}</span>',
            obj.question_text,
            preview,
            "..." if len(obj.question_text) > 80 else "",
        )

    question_preview.short_description = "Question"


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = [
        "question_preview",
        "category",
        "question_type",
        "difficulty",
        "time_limit",
        "is_active",
    ]
    list_filter = ["category", "question_type", "difficulty", "is_active"]
    search_fields = ["question_text", "keywords", "tips"]
    list_editable = ["is_active"]
    list_per_page = 20
    save_on_top = True
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("category", "question_type", "difficulty", "question_text")},
        ),
        (
            "Answer & Evaluation",
            {"fields": ("sample_answer", "keywords", "tips"), "classes": ("wide",)},
        ),
        ("Settings", {"fields": ("time_limit", "is_active")}),
    )

    def question_preview(self, obj):
        preview = obj.question_text[:80]
        return format_html(
            '<span title="{}">{}{}</span>',
            obj.question_text,
            preview,
            "..." if len(obj.question_text) > 80 else "",
        )

    question_preview.short_description = "Question"

    actions = ["activate_questions", "deactivate_questions"]

    def activate_questions(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} questions activated.")

    def deactivate_questions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} questions deactivated.")


@admin.register(UserInterviewProgress)
class UserInterviewProgressAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "question_link",
        "score_display",
        "is_completed",
        "attempted_at",
    ]
    list_filter = ["is_completed", "question__category", "attempted_at"]
    search_fields = ["user__email", "question__question_text"]
    readonly_fields = ["attempted_at", "updated_at"]

    def question_link(self, obj):
        url = reverse(
            "admin:interviews_interviewquestion_change", args=[obj.question.id]
        )
        return format_html('<a href="{}">{}</a>', url, obj.question.question_text[:50])

    question_link.short_description = "Question"

    def score_display(self, obj):
        if obj.score >= 85:
            color = "#10b981"
        elif obj.score >= 70:
            color = "#f59e0b"
        else:
            color = "#ef4444"
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color,
            obj.score,
        )

    score_display.short_description = "Score"
