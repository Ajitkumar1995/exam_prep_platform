from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from django.http import JsonResponse
from .models import (
    ExamCategory,
    Exam,
    Subject,
    Topic,
    StudyMaterial,
    ExamAnnouncement,
    ExamFaq,
    DailyChallenge,
    LiveTestCard,
)
from apps.payments.views import has_payment_access
from apps.mocktests.models import MockTest, TestAttempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.cache.decorators import anonymous_cache_page
from apps.cache.timeouts import CacheTimeout


@anonymous_cache_page(CacheTimeout.EXAM_LIST, key_prefix="exam_list")
def exam_list(request):
    """List all exams grouped by category"""
    categories = ExamCategory.objects.filter(is_active=True).prefetch_related("exams")

    # Get popular exams (with actual data)
    popular_exams = (
        Exam.objects.filter(is_active=True)
        .annotate(
            material_count=Count("study_materials"), question_count=Count("questions")
        )
        .order_by("-material_count", "-question_count")[:8]
    )

    # If no popular exams with questions, show any active exams
    if not popular_exams:
        popular_exams = Exam.objects.filter(is_active=True)[:8]

    # Get live test cards
    live_tests = LiveTestCard.objects.filter(is_active=True).order_by("order")

    # Get daily challenge
    today = timezone.now().date()
    daily_challenge = DailyChallenge.objects.filter(
        is_active=True, challenge_date=today
    ).first()

    # Get featured exams for banner
    featured_exams = Exam.objects.filter(is_active=True)[:3]

    context = {
        "categories": categories,
        "popular_exams": popular_exams,
        "live_tests": live_tests,
        "daily_challenge": daily_challenge,
        "featured_exams": featured_exams,
    }
    return render(request, "exams/list.html", context)


@anonymous_cache_page(CacheTimeout.EXAM_LIST, key_prefix="exam_category")
def category_detail(request, slug):
    """Show details of a specific category"""
    category = get_object_or_404(ExamCategory, slug=slug, is_active=True)
    exams = list(
        Exam.objects.filter(category=category, is_active=True).annotate(
            active_question_count=Count(
                "questions", filter=Q(questions__is_active=True), distinct=True
            ),
            active_mock_test_count=Count(
                "mock_tests", filter=Q(mock_tests__is_active=True), distinct=True
            ),
        )
    )

    context = {
        "category": category,
        "exams": exams,
        "total_exams": len(exams),
        "total_questions": sum(exam.active_question_count for exam in exams),
        "total_mock_tests": sum(exam.active_mock_test_count for exam in exams),
    }
    return render(request, "exams/category_detail.html", context)


@anonymous_cache_page(CacheTimeout.EXAM_DETAIL, key_prefix="exam_detail")
def exam_detail(request, slug):
    """Show detailed information about a specific exam"""
    exam = get_object_or_404(
        Exam.objects.select_related("category"), slug=slug, is_active=True
    )

    # # Check if user has access to paid content
    # if exam.is_paid and exam.price > 0:
    #     if not request.user.is_authenticated:
    #         messages.warning(request, f'Please login to access "{exam.name}"')
    #         return redirect('accounts:login_signup')

    #     if not has_payment_access(request.user, 'exam', exam.id):
    #         messages.info(request, f'Please complete payment to access "{exam.name}"')
    #         return redirect('payments:payment_page', item_type='exam', item_id=exam.id)

    # Get subjects
    subjects = exam.subjects.filter(is_active=True)

    # Get study materials
    study_materials = exam.study_materials.filter(is_active=True)[:6]

    # Get announcements
    announcements = exam.announcements.filter(is_active=True)[:5]

    # Get FAQs
    faqs = exam.faqs.filter(is_active=True)

    # Get related exams
    related_exams = Exam.objects.filter(category=exam.category, is_active=True).exclude(
        id=exam.id
    )[:6]

    total_questions = exam.questions.filter(is_active=True).count()
    total_mock_tests = exam.mock_tests.filter(is_active=True).count()

    # Get free mock test
    free_mock_test = exam.mock_tests.filter(is_active=True, is_paid=True).first()

    context = {
        "exam": exam,
        "subjects": subjects,
        "study_materials": study_materials,
        "announcements": announcements,
        "faqs": faqs,
        "related_exams": related_exams,
        "total_questions": total_questions,
        "total_mock_tests": total_mock_tests,
        "free_mock_test": free_mock_test,
    }
    return render(request, "exams/exam_detail.html", context)


@anonymous_cache_page(CacheTimeout.EXAM_DETAIL, key_prefix="exam_coaching")
def exam_coaching(request, slug):
    """Show coaching details for an exam"""
    exam = get_object_or_404(Exam, slug=slug, is_active=True)

    subjects = list(exam.subjects.filter(is_active=True))
    materials_by_subject = {subject.id: [] for subject in subjects}
    for material in (
        exam.study_materials.filter(is_active=True, subject_id__in=materials_by_subject)
        .select_related("subject")
        .order_by("subject_id", "-created_at")
    ):
        subject_materials = materials_by_subject.get(material.subject_id)
        if subject_materials is not None and len(subject_materials) < 5:
            subject_materials.append(material)

    course_modules = [
        {"subject": subject, "materials": materials_by_subject[subject.id]}
        for subject in subjects
        if materials_by_subject[subject.id]
    ]

    # Count video lectures
    video_lectures_count = exam.study_materials.filter(
        material_type="video", is_active=True
    ).count()

    # Get total mock tests
    total_mock_tests = exam.mock_tests.filter(is_active=True).count()

    # Course pricing (can be stored in Exam model or separate model)
    course_price = getattr(exam, "coaching_price", 4999)
    original_price = getattr(exam, "coaching_original_price", 9999)
    discount_percentage = getattr(exam, "coaching_discount", 50)

    context = {
        "exam": exam,
        "course_modules": course_modules,
        "course_price": course_price,
        "original_price": original_price,
        "discount_percentage": discount_percentage,
        "video_lectures_count": video_lectures_count,
        "total_mock_tests": total_mock_tests,
    }
    return render(request, "exams/exam_coaching.html", context)


@anonymous_cache_page(CacheTimeout.MOCK_TEST_LIST, key_prefix="exam_mock_tests")
def exam_mock_tests(request, slug):
    """Show mock tests for an exam"""
    exam = get_object_or_404(Exam, slug=slug, is_active=True)
    mock_tests = list(exam.mock_tests.filter(is_active=True))

    # Calculate total questions across all mock tests
    total_questions = sum(mt.total_questions for mt in mock_tests)

    # Calculate average rating (if you have a rating model)
    avg_rating = 4.5

    context = {
        "exam": exam,
        "mock_tests": mock_tests,
        "total_questions": total_questions,
        "avg_rating": avg_rating,
    }
    return render(request, "exams/exam_mock_tests.html", context)


@anonymous_cache_page(CacheTimeout.STUDY_MATERIAL, key_prefix="exam_study_material")
def exam_study_material(request, slug):
    """Show study material for an exam"""
    exam = get_object_or_404(Exam, slug=slug, is_active=True)

    materials = list(
        exam.study_materials.filter(is_active=True).select_related("subject")
    )
    notes = [material for material in materials if material.material_type == "notes"]
    videos = [material for material in materials if material.material_type == "video"]
    pdfs = [material for material in materials if material.material_type == "pdf"]
    ebooks = [material for material in materials if material.material_type == "ebook"]
    current_affairs = notes[:5]
    previous_papers = pdfs[:5]
    recommended_books = ebooks[:4]

    context = {
        "exam": exam,
        "notes": notes,
        "videos": videos,
        "pdfs": pdfs,
        "ebooks": ebooks,
        "current_affairs": current_affairs,
        "previous_papers": previous_papers,
        "recommended_books": recommended_books,
    }
    return render(request, "exams/exam_study_material.html", context)


@login_required
def start_free_mock_test(request, exam_slug):
    """Redirect to first free mock test"""
    exam = get_object_or_404(Exam, slug=exam_slug, is_active=True)
    free_mock_test = exam.mock_tests.filter(is_active=True, is_paid=True).first()

    if free_mock_test:
        return redirect("mocktests:take_mock_test", test_id=free_mock_test.id)
    else:
        messages.warning(request, "No free mock test available for this exam yet.")
        return redirect("exams:detail", slug=exam_slug)


@login_required
def enroll_now(request, exam_slug):
    """Handle enrollment for coaching with payment integration"""
    exam = get_object_or_404(Exam, slug=exam_slug, is_active=True)

    # Check if user is already enrolled (if you have enrollment model)
    # existing_enrollment = CourseEnrollment.objects.filter(user=request.user, exam=exam).first()
    # if existing_enrollment:
    #     messages.info(request, f'You are already enrolled in {exam.name} coaching!')
    #     return redirect('exams:coaching_dashboard', exam_slug=exam.slug)

    messages.success(
        request,
        f"Thank you for your interest in {exam.name} coaching! Our team will contact you soon.",
    )
    return redirect("exams:coaching", slug=exam_slug)


def take_daily_challenge(request, challenge_slug):
    """Start daily challenge"""
    challenge = get_object_or_404(DailyChallenge, slug=challenge_slug, is_active=True)

    if challenge.test_url:
        return redirect(challenge.test_url)
    elif challenge.mock_test:
        return redirect("mocktests:take_mock_test", test_id=challenge.mock_test.id)
    else:
        messages.warning(request, "Challenge test is not configured yet.")
        return redirect("exams:list")


def join_live_test(request, test_id):
    """Join a live test from live test card"""
    live_test = get_object_or_404(LiveTestCard, id=test_id, is_active=True)

    # If button_url is provided, redirect there
    if live_test.button_url:
        return redirect(live_test.button_url)

    # Otherwise, try to find a free mock test for the associated exam
    if live_test.exam:
        # Find a free mock test first (no login required)
        mock_test = live_test.exam.mock_tests.filter(
            is_active=True, is_paid=False
        ).first()

        if mock_test:
            # Allow access without login for free tests
            return redirect("mocktests:take_mock_test", test_id=mock_test.id)
        else:
            # If no free test, try paid test but require login
            mock_test = live_test.exam.mock_tests.filter(is_active=True).first()
            if mock_test:
                if request.user.is_authenticated:
                    return redirect(
                        "payments:payment_page",
                        item_type="mock_test",
                        item_id=mock_test.id,
                    )
                else:
                    messages.info(request, "Please login to access this test.")
                    return redirect("accounts:login_signup")

    messages.warning(request, "Test is not available yet. Please check back later.")
    return redirect("exams:list")


@anonymous_cache_page(CacheTimeout.LEADERBOARD, key_prefix="exam_analytics")
def get_exam_analytics(request, slug):
    """Get analytics data for an exam (AJAX)"""
    exam = get_object_or_404(Exam, slug=slug, is_active=True)

    mock_stats = exam.mock_tests.filter(is_active=True).aggregate(
        total_mock_tests=Count("id"),
        total_questions=Sum("total_questions"),
    )
    attempt_stats = TestAttempt.objects.filter(
        mock_test__exam=exam, mock_test__is_active=True, status="completed"
    ).aggregate(total_attempts=Count("id"), average_score=Avg("percentage"))

    data = {
        "total_mock_tests": mock_stats["total_mock_tests"] or 0,
        "total_questions": exam.questions.filter(is_active=True).count(),
        "total_study_materials": exam.study_materials.filter(is_active=True).count(),
        "total_attempts": attempt_stats["total_attempts"] or 0,
        "average_score": round(attempt_stats["average_score"] or 0, 2),
    }
    return JsonResponse(data)
