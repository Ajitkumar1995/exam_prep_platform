from django.contrib import admin
from django.utils.html import format_html
from .models import LiveTestCard
from .models import (
    ExamCategory,
    Exam,
    Subject,
    Topic,
    Question,
    Option,
    ExamAnnouncement,
    ExamFaq,
    StudyMaterial,
)
from .models import DailyChallenge, LeaderboardEntry, ChallengeParticipant


@admin.register(LiveTestCard)
class LiveTestCardAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "subtitle",
        "badge_text",
        "total_participants",
        "enrolled_percentage",
        "is_active",
        "order",
    ]
    list_filter = ["badge_color", "is_active", "is_featured"]
    search_fields = ["title", "subtitle"]
    list_editable = ["enrolled_percentage", "is_active", "order"]
    fieldsets = (
        (
            "Card Content",
            {"fields": ("exam", "title", "subtitle", "badge_text", "badge_color")},
        ),
        ("Statistics", {"fields": ("total_participants", "enrolled_percentage")}),
        (
            "Timer Settings",
            {"fields": ("has_timer", "timer_hours", "timer_minutes", "timer_seconds")},
        ),
        ("Link & Button", {"fields": ("button_text", "button_url")}),
        ("Display Settings", {"fields": ("order", "is_active", "is_featured")}),
        ("Schedule", {"fields": ("start_date", "end_date"), "classes": ("collapse",)}),
    )

    actions = ["activate_cards", "deactivate_cards", "feature_cards"]

    def activate_cards(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} cards activated.")

    def deactivate_cards(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} cards deactivated.")

    def feature_cards(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} cards marked as featured.")


@admin.register(DailyChallenge)
class DailyChallengeAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "challenge_date",
        "challenge_type",
        "difficulty",
        "total_participants",
        "is_active",
        "is_featured",
    ]
    list_filter = [
        "challenge_type",
        "difficulty",
        "is_active",
        "is_featured",
        "challenge_date",
    ]
    search_fields = ["title", "description"]
    list_editable = ["is_active", "is_featured"]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (
            "Challenge Details",
            {
                "fields": (
                    "title",
                    "slug",
                    "description",
                    "challenge_type",
                    "difficulty",
                )
            },
        ),
        (
            "Settings",
            {
                "fields": (
                    "total_questions",
                    "duration_minutes",
                    "xp_reward",
                    "coin_reward",
                )
            },
        ),
        ("Test Link", {"fields": ("test_url", "mock_test")}),
        ("Schedule", {"fields": ("challenge_date", "is_active", "is_featured")}),
        (
            "Statistics",
            {
                "fields": ("total_participants", "total_completed"),
                "classes": ("collapse",),
            },
        ),
    )
    actions = ["activate_challenges", "deactivate_challenges", "feature_challenges"]

    def activate_challenges(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} challenges activated.")

    def deactivate_challenges(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} challenges deactivated.")

    def feature_challenges(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} challenges marked as featured.")


@admin.register(ChallengeParticipant)
class ChallengeParticipantAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "challenge",
        "score",
        "percentage",
        "is_completed",
        "completed_at",
    ]
    list_filter = ["is_completed", "challenge"]
    search_fields = ["user__email", "challenge__title"]
    readonly_fields = ["completed_at"]


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ["user", "exam", "period", "score", "rank", "accuracy", "date"]
    list_filter = ["period", "exam", "date"]
    search_fields = ["user__email", "exam__name"]
    list_editable = ["rank"]


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4
    fields = ["option_text", "option_text_hindi", "is_correct", "order"]
    classes = ["collapse"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "question_text_preview",
        "exam",
        "subject",
        "topic",
        "question_type",
        "difficulty",
        "marks",
        "is_active",
    ]
    list_filter = [
        "exam",
        "subject",
        "topic",
        "question_type",
        "difficulty",
        "is_active",
    ]
    search_fields = ["question_text", "explanation", "tags"]
    list_editable = ["marks", "difficulty", "is_active"]
    list_per_page = 20

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("exam", "subject", "topic", "question_type")},
        ),
        (
            "Question Text",
            {"fields": ("question_text", "question_text_hindi"), "classes": ("wide",)},
        ),
        (
            "Question Settings",
            {"fields": ("difficulty", "marks", "negative_marks", "estimated_time")},
        ),
        (
            "Answer Explanation",
            {
                "fields": ("explanation", "explanation_hindi"),
                "classes": ("wide",),
                "description": "Add detailed explanation for the correct answer. This will help students learn from their mistakes.",
            },
        ),
        ("Media & Tags", {"fields": ("image", "tags"), "classes": ("collapse",)}),
        ("Status", {"fields": ("is_active",), "classes": ("collapse",)}),
    )

    inlines = [OptionInline]
    save_on_top = True

    def question_text_preview(self, obj):
        return (
            obj.question_text[:80] + "..."
            if len(obj.question_text) > 80
            else obj.question_text
        )

    question_text_preview.short_description = "Question"


@admin.register(ExamCategory)
class ExamCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order", "total_exams", "is_active"]
    list_editable = ["order", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    list_filter = ["is_active"]

    def total_exams(self, obj):
        return obj.exams.filter(is_active=True).count()

    total_exams.short_description = "Total Exams"


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "short_name",
        "exam_level",
        "is_paid",
        "price",
        "is_active",
        "order",
    ]
    list_filter = ["category", "exam_level", "is_paid", "is_active"]
    search_fields = ["name", "short_name"]
    list_editable = ["order", "is_active", "is_paid", "price"]
    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "category",
                    "name",
                    "short_name",
                    "slug",
                    "exam_level",
                    "logo",
                    "order",
                )
            },
        ),
        (
            "Description",
            {"fields": ("description", "eligibility", "exam_pattern", "syllabus")},
        ),
        (
            "Exam Details",
            {
                "fields": (
                    "duration_minutes",
                    "total_marks",
                    "total_questions",
                    "negative_marking",
                    "official_website",
                )
            },
        ),
        (
            "Pricing",
            {
                "fields": ("is_paid", "price", "discount_price"),
                "description": "Set if this exam course is paid or free",
            },
        ),
        ("Important Dates", {"fields": ("important_dates",), "classes": ("collapse",)}),
        ("Status", {"fields": ("is_active",)}),
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "exam",
        "code",
        "weightage",
        "total_questions",
        "total_marks",
        "is_active",
        "order",
    ]
    list_filter = ["exam", "is_active"]
    search_fields = ["name", "exam__name"]
    list_editable = [
        "weightage",
        "total_questions",
        "total_marks",
        "is_active",
        "order",
    ]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "subject",
        "difficulty_level",
        "weightage",
        "total_questions",
        "is_active",
        "order",
    ]
    list_filter = ["subject", "difficulty_level", "is_active"]
    search_fields = ["name", "subject__name"]
    list_editable = [
        "difficulty_level",
        "weightage",
        "total_questions",
        "is_active",
        "order",
    ]


@admin.register(ExamAnnouncement)
class ExamAnnouncementAdmin(admin.ModelAdmin):
    list_display = ["title", "exam", "announcement_date", "is_important", "is_active"]
    list_filter = ["exam", "is_important", "is_active"]
    search_fields = ["title", "content"]


@admin.register(ExamFaq)
class ExamFaqAdmin(admin.ModelAdmin):
    list_display = ["question", "exam", "order", "is_active"]
    list_filter = ["exam", "is_active"]
    search_fields = ["question", "answer"]
    list_editable = ["order", "is_active"]


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "exam",
        "subject",
        "material_type",
        "is_free",
        "downloads",
        "views",
        "is_active",
    ]
    list_filter = ["exam", "subject", "material_type", "is_free", "is_active"]
    search_fields = ["title", "description"]
    list_editable = ["is_free", "is_active"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("exam", "subject", "title", "material_type")},
        ),
        (
            "Content",
            {"fields": ("description", "file", "video_url", "thumbnail", "duration")},
        ),
        ("Statistics", {"fields": ("downloads", "views"), "classes": ("collapse",)}),
        ("Status", {"fields": ("is_free", "is_active")}),
    )
