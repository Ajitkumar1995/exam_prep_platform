from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q, Count, Avg, Sum
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.views.generic import RedirectView
from drf_yasg import openapi


def about(request):
    return render(request, "about.html")


def faq(request):
    return render(request, "faq.html")


def privacy_policy(request):
    return render(request, "privacy_policy.html")


# Home page view with notifications, live cards, daily challenge, and leaderboard
def home(request):
    from apps.exams.models import (
        ExamCategory,
        LiveTestCard,
        DailyChallenge,
        ChallengeParticipant,
    )
    from apps.notifications.models import Notification
    from apps.accounts.models import User

    # Get exam categories
    categories = ExamCategory.objects.filter(is_active=True)

    # Get active live test cards
    live_cards = (
        LiveTestCard.objects.filter(is_active=True)
        .filter(Q(start_date__isnull=True) | Q(start_date__lte=timezone.now()))
        .filter(Q(end_date__isnull=True) | Q(end_date__gte=timezone.now()))
        .order_by("-is_featured", "order", "-created_at")[:6]
    )

    # Get today's daily challenge
    today = timezone.now().date()
    daily_challenge = DailyChallenge.objects.filter(
        is_active=True, challenge_date=today
    ).first()

    # If no challenge for today, get the latest active challenge
    if not daily_challenge:
        daily_challenge = (
            DailyChallenge.objects.filter(is_active=True, challenge_date__lte=today)
            .order_by("-challenge_date")
            .first()
        )

    # Get user's challenge participation status
    user_participation = None
    if request.user.is_authenticated and daily_challenge:
        user_participation = ChallengeParticipant.objects.filter(
            challenge=daily_challenge, user=request.user
        ).first()

    # Get dynamic leaderboard (top 5 users by test performance)
    leaderboard_users = (
        User.objects.filter(test_attempts__status="completed")
        .annotate(
            avg_score=Avg("test_attempts__percentage"),
            total_tests=Count("test_attempts"),
            total_correct=Sum("test_attempts__correct_answers"),
        )
        .order_by("-avg_score")[:5]
    )

    leaderboard = []
    for idx, user in enumerate(leaderboard_users, 1):
        # Get user's exam preference or default exam
        exam_name = "General"
        if user.test_attempts.filter(status="completed").exists():
            exam_name = (
                user.test_attempts.filter(status="completed")
                .first()
                .mock_test.exam.name
            )

        leaderboard.append(
            {
                "rank": idx,
                "name": user.get_full_name() or user.username,
                "exam": exam_name,
                "score": round(user.avg_score, 1) if user.avg_score else 0,
                "accuracy": (
                    round((user.total_correct / (user.total_tests * 100)) * 100, 1)
                    if user.total_tests and user.total_correct
                    else 0
                ),
            }
        )

    # Get active notifications for homepage
    notifications = (
        Notification.objects.filter(
            is_active=True, show_on_homepage=True, start_date__lte=timezone.now()
        )
        .filter(Q(end_date__isnull=True) | Q(end_date__gte=timezone.now()))
        .order_by("-order", "-created_at")[:6]
    )

    context = {
        "exam_categories": categories,
        "user": request.user,
        "notifications": notifications,
        "live_cards": live_cards,
        "daily_challenge": daily_challenge,
        "user_participation": user_participation,
        "leaderboard": leaderboard,
    }
    return render(request, "index.html", context)


schema_view = get_schema_view(
    openapi.Info(
        title="Exam Preparation Platform API",
        default_version="v1",
        description="API for Government Competitive Exam Preparation Platform",
        terms_of_service="https://www.govtexamwala.com/privacy-policy/",
        # contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("faq/", faq, name="faq"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),
    path("api/", include("apps.api.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("exams/", include("apps.exams.urls")),
    path("mock-tests/", include("apps.mocktests.urls")),
    path("analytics/", include("apps.analytics.urls")),
    path("interviews/", include("apps.interviews.urls")),
    path("study/", include("apps.study_materials.urls")),
    path("payments/", include("apps.payments.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("accounts/", RedirectView.as_view(url="/accounts/auth/", permanent=True)),
    path("contact/", include("apps.contact.urls")),
    # Swagger documentation
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
