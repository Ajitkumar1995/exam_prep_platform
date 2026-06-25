from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Q
from django.utils import timezone
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
from apps.mocktests.models import MockTest
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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


def category_detail(request, slug):
    """Show details of a specific category"""
    category = get_object_or_404(ExamCategory, slug=slug, is_active=True)
    exams = Exam.objects.filter(category=category, is_active=True)

    # Calculate statistics
    total_questions = 0
    total_mock_tests = 0
    for exam in exams:
        total_questions += exam.questions.filter(is_active=True).count()
        total_mock_tests += exam.mock_tests.filter(is_active=True).count()

    context = {
        "category": category,
        "exams": exams,
        "total_exams": exams.count(),
        "total_questions": total_questions,
        "total_mock_tests": total_mock_tests,
    }
    return render(request, "exams/category_detail.html", context)


def exam_detail(request, slug):
    """Show detailed information about a specific exam"""
    exam = get_object_or_404(Exam, slug=slug, is_active=True)

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

    # Get statistics
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


def exam_coaching(request, slug):
    """Show coaching details for an exam"""
    exam = get_object_or_404(Exam, slug=slug, is_active=True)

    # Get course modules from study materials grouped by subject
    course_modules = []
    subjects = exam.subjects.filter(is_active=True)
    for subject in subjects:
        materials = exam.study_materials.filter(subject=subject, is_active=True)[:5]
        if materials.exists():
            course_modules.append({"subject": subject, "materials": materials})

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


def exam_mock_tests(request, slug):
    """Show mock tests for an exam"""
    exam = get_object_or_404(Exam, slug=slug, is_active=True)
    mock_tests = exam.mock_tests.filter(is_active=True)

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


def exam_study_material(request, slug):
    """Show study material for an exam"""
    exam = get_object_or_404(Exam, slug=slug, is_active=True)

    # Filter study materials by type
    notes = exam.study_materials.filter(material_type="notes", is_active=True)
    videos = exam.study_materials.filter(material_type="video", is_active=True)
    pdfs = exam.study_materials.filter(material_type="pdf", is_active=True)
    ebooks = exam.study_materials.filter(material_type="ebook", is_active=True)

    # Current affairs (you can add a separate model or use notes with a tag)
    current_affairs = exam.study_materials.filter(
        material_type="notes", is_active=True
    )[:5]

    # Previous year papers (you can add a separate model or use pdfs with tag)
    previous_papers = exam.study_materials.filter(material_type="pdf", is_active=True)[
        :5
    ]

    # Recommended books (ebooks)
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


# def join_live_test(request, test_id):
#     """Join a live test from live test card"""
#     live_test = get_object_or_404(LiveTestCard, id=test_id, is_active=True)

#     # If button_url is provided, redirect there
#     if live_test.button_url:
#         return redirect(live_test.button_url)

#     # Otherwise, try to find a mock test for the associated exam
#     if live_test.exam:
#         # mock_test = live_test.exam.mock_tests.filter(is_active=True).first()
#         mock_test = live_test.exam.mock_tests.filter(is_active=True, is_paid=False).first()
#         if mock_test:
#             if request.user.is_authenticated:
#                 return redirect('mocktests:take_mock_test', test_id=mock_test.id)
#             else:
#                 messages.info(request, 'Please login to take this test.')
#                 return redirect('accounts:login_signup')

#     messages.warning(request, 'Test is not available yet. Please check back later.')
#     return redirect('exams:list')


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


def get_exam_analytics(request, slug):
    """Get analytics data for an exam (AJAX)"""
    exam = get_object_or_404(Exam, slug=slug, is_active=True)

    # Get mock test statistics
    mock_tests = exam.mock_tests.filter(is_active=True)
    total_attempts = 0
    avg_score = 0

    for mock_test in mock_tests:
        attempts = mock_test.attempts.filter(status="completed")
        total_attempts += attempts.count()
        avg = attempts.aggregate(Avg("percentage"))["percentage__avg"] or 0
        avg_score = (avg_score + avg) / 2 if avg_score else avg

    data = {
        "total_mock_tests": mock_tests.count(),
        "total_questions": exam.questions.filter(is_active=True).count(),
        "total_study_materials": exam.study_materials.filter(is_active=True).count(),
        "total_attempts": total_attempts,
        "average_score": round(avg_score, 2),
    }
    return JsonResponse(data)
