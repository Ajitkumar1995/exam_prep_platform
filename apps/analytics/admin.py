from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import (
    UserPerformance,
    ExamPerformance,
    SubjectPerformance,
    TopicPerformance,
    DailyActivity,
)


@admin.register(UserPerformance)
class UserPerformanceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user_link",
        "total_tests_taken",
        "overall_accuracy_display",
        "average_score_display",
        "rank",
        "percentile_display",
        "last_updated",
    ]
    list_filter = ["rank", "last_updated"]
    search_fields = [
        "user__email",
        "user__username",
        "user__first_name",
        "user__last_name",
    ]
    readonly_fields = [
        "total_tests_taken",
        "total_questions_attempted",
        "total_correct_answers",
        "total_wrong_answers",
        "total_skipped_answers",
        "overall_accuracy",
        "average_score",
        "total_time_spent",
        "rank",
        "percentile",
        "last_updated",
        "user_link",
        "overall_accuracy_display",
        "average_score_display",
        "percentile_display",
        "time_spent_display",
    ]

    def user_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html(
            '<a href="{}" style="font-weight: bold;">{} ({})</a>',
            url,
            obj.user.get_full_name() or obj.user.username,
            obj.user.email,
        )

    user_link.short_description = "User"

    def overall_accuracy_display(self, obj):
        color = (
            "#10b981"
            if obj.overall_accuracy >= 70
            else "#f59e0b" if obj.overall_accuracy >= 40 else "#ef4444"
        )
        return mark_safe(
            f'<span style="color: {color}; font-weight: bold;">{obj.overall_accuracy:.1f}%</span>'
        )

    overall_accuracy_display.short_description = "Overall Accuracy"

    def average_score_display(self, obj):
        color = (
            "#10b981"
            if obj.average_score >= 70
            else "#f59e0b" if obj.average_score >= 40 else "#ef4444"
        )
        return mark_safe(
            f'<span style="color: {color}; font-weight: bold;">{obj.average_score:.1f}%</span>'
        )

    average_score_display.short_description = "Average Score"

    def percentile_display(self, obj):
        return mark_safe(
            f'<span style="font-weight: bold;">{obj.percentile:.1f}%</span>'
        )

    percentile_display.short_description = "Percentile"

    def time_spent_display(self, obj):
        hours = obj.total_time_spent // 3600
        minutes = (obj.total_time_spent % 3600) // 60
        return f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"

    time_spent_display.short_description = "Total Time Spent"

    actions = ["refresh_stats"]

    def refresh_stats(self, request, queryset):
        for performance in queryset:
            performance.update_stats()
        self.message_user(
            request, f"Statistics refreshed for {queryset.count()} user(s)."
        )

    refresh_stats.short_description = "Refresh selected user statistics"


@admin.register(ExamPerformance)
class ExamPerformanceAdmin(admin.ModelAdmin):
    list_display = [
        "user_link",
        "exam_link",
        "total_attempts",
        "accuracy_display",
        "average_score_display",
        "best_score_display",
    ]
    list_filter = ["exam", "last_attempt_date"]
    search_fields = ["user__email", "exam__name"]
    readonly_fields = [
        "total_attempts",
        "total_correct",
        "total_wrong",
        "total_skipped",
        "accuracy",
        "average_score",
        "best_score",
    ]

    def user_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)

    user_link.short_description = "User"

    def exam_link(self, obj):
        url = reverse("admin:exams_exam_change", args=[obj.exam.id])
        return format_html('<a href="{}">{}</a>', url, obj.exam.name)

    exam_link.short_description = "Exam"

    def accuracy_display(self, obj):
        color = (
            "#10b981"
            if obj.accuracy >= 70
            else "#f59e0b" if obj.accuracy >= 40 else "#ef4444"
        )
        return mark_safe(
            f'<span style="color: {color}; font-weight: bold;">{obj.accuracy:.1f}%</span>'
        )

    accuracy_display.short_description = "Accuracy"

    def average_score_display(self, obj):
        return mark_safe(
            f'<span style="font-weight: bold;">{obj.average_score:.1f}%</span>'
        )

    average_score_display.short_description = "Avg Score"

    def best_score_display(self, obj):
        return mark_safe(
            f'<span style="color: #10b981; font-weight: bold;">{obj.best_score:.1f}%</span>'
        )

    best_score_display.short_description = "Best Score"


@admin.register(SubjectPerformance)
class SubjectPerformanceAdmin(admin.ModelAdmin):
    list_display = [
        "user_link",
        "subject_link",
        "total_questions",
        "accuracy_display",
        "average_time_display",
    ]
    list_filter = ["subject__exam", "last_updated"]
    search_fields = ["user__email", "subject__name"]

    def user_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)

    user_link.short_description = "User"

    def subject_link(self, obj):
        url = reverse("admin:exams_subject_change", args=[obj.subject.id])
        return format_html(
            '<a href="{}">{} ({})</a>', url, obj.subject.name, obj.subject.exam.name
        )

    subject_link.short_description = "Subject"

    def accuracy_display(self, obj):
        color = (
            "#10b981"
            if obj.accuracy >= 70
            else "#f59e0b" if obj.accuracy >= 40 else "#ef4444"
        )
        return mark_safe(
            f'<span style="color: {color}; font-weight: bold;">{obj.accuracy:.1f}%</span>'
        )

    accuracy_display.short_description = "Accuracy"

    def average_time_display(self, obj):
        return mark_safe(f"<span>{obj.average_time:.1f} seconds</span>")

    average_time_display.short_description = "Avg Time"


@admin.register(TopicPerformance)
class TopicPerformanceAdmin(admin.ModelAdmin):
    list_display = [
        "user_link",
        "topic_link",
        "total_questions",
        "accuracy_display",
        "weak_badge",
        "strong_badge",
    ]
    list_filter = ["is_weak", "is_strong", "topic__subject__exam"]
    search_fields = ["user__email", "topic__name"]

    def user_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)

    user_link.short_description = "User"

    def topic_link(self, obj):
        url = reverse("admin:exams_topic_change", args=[obj.topic.id])
        return format_html(
            '<a href="{}">{} ({})</a>', url, obj.topic.name, obj.topic.subject.name
        )

    topic_link.short_description = "Topic"

    def accuracy_display(self, obj):
        color = (
            "#10b981"
            if obj.accuracy >= 70
            else "#f59e0b" if obj.accuracy >= 40 else "#ef4444"
        )
        return mark_safe(
            f'<span style="color: {color}; font-weight: bold;">{obj.accuracy:.1f}%</span>'
        )

    accuracy_display.short_description = "Accuracy"

    def weak_badge(self, obj):
        if obj.is_weak:
            return mark_safe(
                '<span style="background: #ef4444; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">⚠️ WEAK</span>'
            )
        return mark_safe('<span style="color: #9ca3af;">-</span>')

    weak_badge.short_description = "Weak Area"

    def strong_badge(self, obj):
        if obj.is_strong:
            return mark_safe(
                '<span style="background: #10b981; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">💪 STRONG</span>'
            )
        return mark_safe('<span style="color: #9ca3af;">-</span>')

    strong_badge.short_description = "Strong Area"


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = [
        "user_link",
        "date",
        "tests_taken",
        "questions_attempted",
        "correct_rate_display",
        "streak_badge",
    ]
    list_filter = ["date", "streak"]
    search_fields = ["user__email", "user__username"]
    date_hierarchy = "date"

    def user_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)

    user_link.short_description = "User"

    def correct_rate_display(self, obj):
        if obj.questions_attempted > 0:
            rate = (obj.correct_answers / obj.questions_attempted) * 100
            color = "#10b981" if rate >= 70 else "#f59e0b" if rate >= 40 else "#ef4444"
            return mark_safe(
                f'<span style="color: {color}; font-weight: bold;">{rate:.1f}%</span>'
            )
        return mark_safe('<span style="color: #9ca3af;">-</span>')

    correct_rate_display.short_description = "Correct Rate"

    def streak_badge(self, obj):
        if obj.streak >= 30:
            return mark_safe(
                f'<span style="background: #8b5cf6; color: white; padding: 2px 8px; border-radius: 12px;">🔥 {obj.streak}</span>'
            )
        elif obj.streak >= 7:
            return mark_safe(
                f'<span style="background: #f59e0b; color: white; padding: 2px 8px; border-radius: 12px;">⚡ {obj.streak}</span>'
            )
        elif obj.streak > 0:
            return mark_safe(
                f'<span style="background: #10b981; color: white; padding: 2px 8px; border-radius: 12px;">📅 {obj.streak}</span>'
            )
        return mark_safe('<span style="color: #9ca3af;">-</span>')

    streak_badge.short_description = "Streak"


# from django.contrib import admin
# from django.utils.html import format_html
# from django.utils.safestring import mark_safe
# from django.urls import reverse
# from .models import (
#     UserPerformance,
#     ExamPerformance,
#     SubjectPerformance,
#     TopicPerformance,
#     DailyActivity
# )


# @admin.register(UserPerformance)
# class UserPerformanceAdmin(admin.ModelAdmin):
#     """Admin for overall user performance"""

#     list_display = [
#         'id',
#         'user_link',
#         'total_tests_taken',
#         'overall_accuracy_display',
#         'average_score_display',
#         'rank',
#         'percentile_display',
#         'last_updated'
#     ]

#     list_filter = [
#         'rank',
#         'last_updated'
#     ]

#     search_fields = [
#         'user__email',
#         'user__username',
#         'user__first_name',
#         'user__last_name'
#     ]

#     readonly_fields = [
#         'total_tests_taken',
#         'total_questions_attempted',
#         'total_correct_answers',
#         'total_wrong_answers',
#         'total_skipped_answers',
#         'overall_accuracy',
#         'average_score',
#         'total_time_spent',
#         'rank',
#         'percentile',
#         'last_updated',
#         'user_link',
#         'overall_accuracy_display',
#         'average_score_display',
#         'percentile_display',
#         'time_spent_display'
#     ]

#     fieldsets = (
#         ('User Information', {
#             'fields': ('user_link',)
#         }),
#         ('Statistics', {
#             'fields': (
#                 'total_tests_taken',
#                 'total_questions_attempted',
#                 'total_correct_answers',
#                 'total_wrong_answers',
#                 'total_skipped_answers'
#             ),
#             'classes': ('wide',)
#         }),
#         ('Performance Metrics', {
#             'fields': (
#                 'overall_accuracy_display',
#                 'average_score_display',
#                 'time_spent_display',
#                 'rank',
#                 'percentile_display'
#             ),
#             'classes': ('wide',)
#         }),
#         ('Meta Information', {
#             'fields': ('last_updated',),
#             'classes': ('collapse',)
#         }),
#     )

#     def user_link(self, obj):
#         """Display user with link to user admin"""
#         url = reverse('admin:accounts_user_change', args=[obj.user.id])
#         return format_html('<a href="{}" style="font-weight: bold;">{} ({})</a>',
#                           url, obj.user.get_full_name() or obj.user.username, obj.user.email)
#     user_link.short_description = 'User'
#     user_link.admin_order_field = 'user__username'

#     def overall_accuracy_display(self, obj):
#         try:
#             accuracy = float(obj.overall_accuracy)
#         except (TypeError, ValueError):
#             accuracy = 0.0
#         color = '#10b981' if accuracy >= 70 else '#f59e0b' if accuracy >= 40 else '#ef4444'
#         return mark_safe(f'<span style="color: {color}; font-weight: bold;">{accuracy:.1f}%</span>')
#     overall_accuracy_display.short_description = 'Overall Accuracy'

#     def average_score_display(self, obj):
#         try:
#             score = float(obj.average_score)
#         except (TypeError, ValueError):
#             score = 0.0
#         color = '#10b981' if score >= 70 else '#f59e0b' if score >= 40 else '#ef4444'
#         return mark_safe(f'<span style="color: {color}; font-weight: bold;">{score:.1f}%</span>')
#     average_score_display.short_description = 'Average Score'

#     def percentile_display(self, obj):
#         try:
#             percentile = float(obj.percentile)
#         except (TypeError, ValueError):
#             percentile = 0.0
#         return mark_safe(f'<span style="font-weight: bold;">{percentile:.1f}%</span>')
#     percentile_display.short_description = 'Percentile'

#     def time_spent_display(self, obj):
#         """Display time spent in hours/minutes"""
#         hours = obj.total_time_spent // 3600
#         minutes = (obj.total_time_spent % 3600) // 60
#         if hours > 0:
#             return f"{hours}h {minutes}m"
#         return f"{minutes}m"
#     time_spent_display.short_description = 'Total Time Spent'

#     actions = ['refresh_stats']

#     def refresh_stats(self, request, queryset):
#         """Refresh statistics for selected users"""
#         for performance in queryset:
#             performance.update_stats()
#         self.message_user(request, f'Statistics refreshed for {queryset.count()} user(s).')
#     refresh_stats.short_description = "Refresh selected user statistics"

#     def has_add_permission(self, request):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False


# @admin.register(ExamPerformance)
# class ExamPerformanceAdmin(admin.ModelAdmin):
#     """Admin for exam-specific performance"""

#     list_display = [
#         'id',
#         'user_link',
#         'exam_link',
#         'total_attempts',
#         'accuracy_display',
#         'average_score_display',
#         'best_score_display',
#         'last_attempt_date'
#     ]

#     list_filter = [
#         'exam',
#         'last_attempt_date'
#     ]

#     search_fields = [
#         'user__email',
#         'user__username',
#         'exam__name'
#     ]

#     readonly_fields = [
#         'total_attempts',
#         'total_correct',
#         'total_wrong',
#         'total_skipped',
#         'accuracy',
#         'average_score',
#         'best_score',
#         'last_attempt_date',
#         'user_link',
#         'exam_link',
#         'accuracy_display',
#         'average_score_display',
#         'best_score_display'
#     ]

#     fieldsets = (
#         ('User & Exam', {
#             'fields': ('user_link', 'exam_link')
#         }),
#         ('Attempt Statistics', {
#             'fields': ('total_attempts', 'total_correct', 'total_wrong', 'total_skipped')
#         }),
#         ('Performance Metrics', {
#             'fields': ('accuracy_display', 'average_score_display', 'best_score_display')
#         }),
#         ('Last Activity', {
#             'fields': ('last_attempt_date',),
#             'classes': ('collapse',)
#         }),
#     )

#     def user_link(self, obj):
#         url = reverse('admin:accounts_user_change', args=[obj.user.id])
#         return format_html('<a href="{}">{}</a>', url, obj.user.email)
#     user_link.short_description = 'User'
#     user_link.admin_order_field = 'user__email'

#     def exam_link(self, obj):
#         url = reverse('admin:exams_exam_change', args=[obj.exam.id])
#         return format_html('<a href="{}">{}</a>', url, obj.exam.name)
#     exam_link.short_description = 'Exam'
#     exam_link.admin_order_field = 'exam__name'

#     def accuracy_display(self, obj):
#         try:
#             accuracy = float(obj.accuracy)
#         except (TypeError, ValueError):
#             accuracy = 0.0
#         color = '#10b981' if accuracy >= 70 else '#f59e0b' if accuracy >= 40 else '#ef4444'
#         return mark_safe(f'<span style="color: {color}; font-weight: bold;">{accuracy:.1f}%</span>')
#     accuracy_display.short_description = 'Accuracy'

#     def average_score_display(self, obj):
#         try:
#             score = float(obj.average_score)
#         except (TypeError, ValueError):
#             score = 0.0
#         return mark_safe(f'<span style="font-weight: bold;">{score:.1f}%</span>')
#     average_score_display.short_description = 'Avg Score'

#     def best_score_display(self, obj):
#         try:
#             score = float(obj.best_score)
#         except (TypeError, ValueError):
#             score = 0.0
#         return mark_safe(f'<span style="color: #10b981; font-weight: bold;">{score:.1f}%</span>')
#     best_score_display.short_description = 'Best Score'

#     actions = ['refresh_stats']

#     def refresh_stats(self, request, queryset):
#         for exam_perf in queryset:
#             exam_perf.update_stats()
#         self.message_user(request, f'Statistics refreshed for {queryset.count()} exam performance(s).')
#     refresh_stats.short_description = "Refresh selected statistics"

#     def has_add_permission(self, request):
#         return False


# @admin.register(SubjectPerformance)
# class SubjectPerformanceAdmin(admin.ModelAdmin):
#     """Admin for subject-wise performance"""

#     list_display = [
#         'id',
#         'user_link',
#         'subject_link',
#         'total_questions',
#         'accuracy_display',
#         'average_time_display',
#         'last_updated'
#     ]

#     list_filter = [
#         'subject__exam',
#         'last_updated'
#     ]

#     search_fields = [
#         'user__email',
#         'user__username',
#         'subject__name'
#     ]

#     readonly_fields = [
#         'total_questions',
#         'correct_answers',
#         'wrong_answers',
#         'accuracy',
#         'average_time',
#         'last_updated',
#         'user_link',
#         'subject_link',
#         'accuracy_display',
#         'average_time_display'
#     ]

#     fieldsets = (
#         ('User & Subject', {
#             'fields': ('user_link', 'subject_link')
#         }),
#         ('Question Statistics', {
#             'fields': ('total_questions', 'correct_answers', 'wrong_answers')
#         }),
#         ('Performance Metrics', {
#             'fields': ('accuracy_display', 'average_time_display')
#         }),
#         ('Meta', {
#             'fields': ('last_updated',),
#             'classes': ('collapse',)
#         }),
#     )

#     def user_link(self, obj):
#         url = reverse('admin:accounts_user_change', args=[obj.user.id])
#         return format_html('<a href="{}">{}</a>', url, obj.user.email)
#     user_link.short_description = 'User'

#     def subject_link(self, obj):
#         url = reverse('admin:exams_subject_change', args=[obj.subject.id])
#         return format_html('<a href="{}">{} ({})</a>', url, obj.subject.name, obj.subject.exam.name)
#     subject_link.short_description = 'Subject'

#     def accuracy_display(self, obj):
#         try:
#             accuracy = float(obj.accuracy)
#         except (TypeError, ValueError):
#             accuracy = 0.0
#         color = '#10b981' if accuracy >= 70 else '#f59e0b' if accuracy >= 40 else '#ef4444'
#         return mark_safe(f'<span style="color: {color}; font-weight: bold;">{accuracy:.1f}%</span>')
#     accuracy_display.short_description = 'Accuracy'

#     def average_time_display(self, obj):
#         try:
#             avg_time = float(obj.average_time)
#         except (TypeError, ValueError):
#             avg_time = 0.0
#         return mark_safe(f'<span>{avg_time:.1f} seconds</span>')
#     average_time_display.short_description = 'Avg Time'

#     actions = ['refresh_stats']

#     def refresh_stats(self, request, queryset):
#         for subject_perf in queryset:
#             subject_perf.update_stats()
#         self.message_user(request, f'Statistics refreshed for {queryset.count()} subject performance(s).')
#     refresh_stats.short_description = "Refresh selected statistics"

#     def has_add_permission(self, request):
#         return False


# @admin.register(TopicPerformance)
# class TopicPerformanceAdmin(admin.ModelAdmin):
#     """Admin for topic-wise performance"""

#     list_display = [
#         'id',
#         'user_link',
#         'topic_link',
#         'total_questions',
#         'accuracy_display',
#         'weak_badge',
#         'strong_badge',
#         'last_updated'
#     ]

#     list_filter = [
#         'is_weak',
#         'is_strong',
#         'topic__subject__exam',
#         'last_updated'
#     ]

#     search_fields = [
#         'user__email',
#         'user__username',
#         'topic__name'
#     ]

#     readonly_fields = [
#         'total_questions',
#         'correct_answers',
#         'wrong_answers',
#         'accuracy',
#         'average_time',
#         'is_weak',
#         'is_strong',
#         'last_updated',
#         'user_link',
#         'topic_link',
#         'accuracy_display',
#         'weak_badge',
#         'strong_badge',
#         'average_time_display'
#     ]

#     fieldsets = (
#         ('User & Topic', {
#             'fields': ('user_link', 'topic_link')
#         }),
#         ('Question Statistics', {
#             'fields': ('total_questions', 'correct_answers', 'wrong_answers')
#         }),
#         ('Performance Metrics', {
#             'fields': ('accuracy_display', 'average_time_display', 'weak_badge', 'strong_badge')
#         }),
#         ('Meta', {
#             'fields': ('last_updated',),
#             'classes': ('collapse',)
#         }),
#     )

#     def user_link(self, obj):
#         url = reverse('admin:accounts_user_change', args=[obj.user.id])
#         return format_html('<a href="{}">{}</a>', url, obj.user.email)
#     user_link.short_description = 'User'

#     def topic_link(self, obj):
#         url = reverse('admin:exams_topic_change', args=[obj.topic.id])
#         return format_html('<a href="{}">{} ({})</a>', url, obj.topic.name, obj.topic.subject.name)
#     topic_link.short_description = 'Topic'

#     def accuracy_display(self, obj):
#         try:
#             accuracy = float(obj.accuracy)
#         except (TypeError, ValueError):
#             accuracy = 0.0
#         color = '#10b981' if accuracy >= 70 else '#f59e0b' if accuracy >= 40 else '#ef4444'
#         return mark_safe(f'<span style="color: {color}; font-weight: bold;">{accuracy:.1f}%</span>')
#     accuracy_display.short_description = 'Accuracy'

#     def average_time_display(self, obj):
#         try:
#             avg_time = float(obj.average_time)
#         except (TypeError, ValueError):
#             avg_time = 0.0
#         return mark_safe(f'<span>{avg_time:.1f} seconds</span>')
#     average_time_display.short_description = 'Avg Time'

#     def weak_badge(self, obj):
#         if obj.is_weak:
#             return mark_safe('<span style="background: #ef4444; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">⚠️ WEAK</span>')
#         return mark_safe('<span style="color: #9ca3af;">-</span>')
#     weak_badge.short_description = 'Weak Area'

#     def strong_badge(self, obj):
#         if obj.is_strong:
#             return mark_safe('<span style="background: #10b981; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">💪 STRONG</span>')
#         return mark_safe('<span style="color: #9ca3af;">-</span>')
#     strong_badge.short_description = 'Strong Area'

#     actions = ['refresh_stats', 'mark_as_weak', 'mark_as_strong']

#     def refresh_stats(self, request, queryset):
#         for topic_perf in queryset:
#             topic_perf.update_stats()
#         self.message_user(request, f'Statistics refreshed for {queryset.count()} topic performance(s).')
#     refresh_stats.short_description = "Refresh selected statistics"

#     def mark_as_weak(self, request, queryset):
#         queryset.update(is_weak=True, is_strong=False)
#         self.message_user(request, f'{queryset.count()} topic(s) marked as weak.')
#     mark_as_weak.short_description = "Mark selected as weak areas"

#     def mark_as_strong(self, request, queryset):
#         queryset.update(is_strong=True, is_weak=False)
#         self.message_user(request, f'{queryset.count()} topic(s) marked as strong.')
#     mark_as_strong.short_description = "Mark selected as strong areas"

#     def has_add_permission(self, request):
#         return False


# @admin.register(DailyActivity)
# class DailyActivityAdmin(admin.ModelAdmin):
#     """Admin for daily user activity tracking"""

#     list_display = [
#         'id',
#         'user_link',
#         'date',
#         'tests_taken',
#         'questions_attempted',
#         'correct_rate_display',
#         'time_spent_display',
#         'streak_badge'
#     ]

#     list_filter = [
#         'date',
#         'streak',
#         'tests_taken'
#     ]

#     search_fields = [
#         'user__email',
#         'user__username'
#     ]

#     date_hierarchy = 'date'

#     readonly_fields = [
#         'tests_taken',
#         'questions_attempted',
#         'correct_answers',
#         'wrong_answers',
#         'time_spent',
#         'streak',
#         'user_link',
#         'correct_rate_display',
#         'time_spent_display',
#         'streak_badge'
#     ]

#     fieldsets = (
#         ('User & Date', {
#             'fields': ('user_link', 'date')
#         }),
#         ('Activity Statistics', {
#             'fields': ('tests_taken', 'questions_attempted', 'correct_answers', 'wrong_answers')
#         }),
#         ('Performance Metrics', {
#             'fields': ('correct_rate_display', 'time_spent_display', 'streak_badge')
#         }),
#     )

#     def user_link(self, obj):
#         url = reverse('admin:accounts_user_change', args=[obj.user.id])
#         return format_html('<a href="{}">{}</a>', url, obj.user.email)
#     user_link.short_description = 'User'
#     user_link.admin_order_field = 'user__email'

#     def correct_rate_display(self, obj):
#         if obj.questions_attempted > 0:
#             rate = (obj.correct_answers / obj.questions_attempted) * 100
#             color = '#10b981' if rate >= 70 else '#f59e0b' if rate >= 40 else '#ef4444'
#             return mark_safe(f'<span style="color: {color}; font-weight: bold;">{rate:.1f}%</span>')
#         return mark_safe('<span style="color: #9ca3af;">-</span>')
#     correct_rate_display.short_description = 'Correct Rate'

#     def time_spent_display(self, obj):
#         minutes = obj.time_spent // 60
#         seconds = obj.time_spent % 60
#         if minutes > 0:
#             return f"{minutes}m {seconds}s"
#         return f"{seconds}s"
#     time_spent_display.short_description = 'Time Spent'

#     def streak_badge(self, obj):
#         if obj.streak >= 30:
#             return mark_safe(f'<span style="background: #8b5cf6; color: white; padding: 2px 8px; border-radius: 12px;">🔥 {obj.streak}</span>')
#         elif obj.streak >= 7:
#             return mark_safe(f'<span style="background: #f59e0b; color: white; padding: 2px 8px; border-radius: 12px;">⚡ {obj.streak}</span>')
#         elif obj.streak > 0:
#             return mark_safe(f'<span style="background: #10b981; color: white; padding: 2px 8px; border-radius: 12px;">📅 {obj.streak}</span>')
#         return mark_safe('<span style="color: #9ca3af;">-</span>')
#     streak_badge.short_description = 'Streak'

#     def has_add_permission(self, request):
#         return False


# # Admin site customization
# admin.site.site_header = 'GovtExamWala Analytics Administration'
# admin.site.site_title = 'GovtExamWala Analytics'
# admin.site.index_title = 'Welcome to GovtExamWala Analytics Dashboard'
