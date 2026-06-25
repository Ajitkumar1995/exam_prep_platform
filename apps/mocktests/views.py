from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Count, Avg, Q, Sum
from django.core.paginator import Paginator
from .models import MockTest, TestAttempt, TestAnswer, MockTestQuestion
from apps.exams.models import Question, Option
from apps.analytics.models import UserPerformance, TopicPerformance, DailyActivity
from apps.payments.views import has_payment_access
from datetime import date
import json
import random
import uuid
from django.shortcuts import redirect
from django.contrib import messages


def add_to_cart_redirect(request, mock_test_id):
    """Redirect to the database cart system"""
    return redirect("payments:add_to_cart", item_type="mock_test", item_id=mock_test_id)


def mock_test_list(request):
    """List all available mock tests"""
    mock_tests = MockTest.objects.filter(is_active=True).select_related("exam")

    # Search functionality in backend (optional - for page reload search)
    search_query = request.GET.get("q")
    if search_query:
        mock_tests = mock_tests.filter(
            Q(name__icontains=search_query)
            | Q(exam__name__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    paginator = Paginator(mock_tests, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Mark free tests
    for test in page_obj:
        test.is_free = not test.is_paid or test.price == 0

    context = {
        "mock_tests": page_obj,
        "search_query": search_query,
    }
    return render(request, "mocktests/list.html", context)


# def mock_test_list(request):
#     """List all available mock tests"""
#     mock_tests = MockTest.objects.filter(is_active=True).select_related('exam')

#     # Search
#     search_query = request.GET.get('q')
#     if search_query:
#         mock_tests = mock_tests.filter(
#             Q(name__icontains=search_query) |
#             Q(exam__name__icontains=search_query)
#         )

#     paginator = Paginator(mock_tests, 12)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Get user's attempted tests
#     attempted_tests = []
#     if request.user.is_authenticated:
#         attempted_tests = TestAttempt.objects.filter(
#             user=request.user,
#             status='completed'
#         ).values_list('mock_test_id', flat=True)

#     context = {
#         'mock_tests': page_obj,
#         'attempted_tests': list(attempted_tests),
#         'search_query': search_query,
#     }
#     return render(request, 'mocktests/list.html', context)


# def mock_test_detail(request, slug):
#     """Show details of a specific mock test"""
#     mock_test = get_object_or_404(MockTest, slug=slug, is_active=True)

#     # Check if user has access to paid content
#     if mock_test.is_paid and mock_test.price > 0:
#         if not request.user.is_authenticated:
#             messages.warning(request, f'Please login to access "{mock_test.name}"')
#             return redirect('accounts:login_signup')

#         if not has_payment_access(request.user, 'mock_test', mock_test.id):
#             messages.info(request, f'Please complete payment to access "{mock_test.name}"')
#             return redirect('payments:payment_page', item_type='mock_test', item_id=mock_test.id)

#     # Check if user has already attempted
#     previous_attempt = None
#     if request.user.is_authenticated:
#         previous_attempt = TestAttempt.objects.filter(
#             user=request.user,
#             mock_test=mock_test,
#             status='completed'
#         ).first()

#     # Get statistics
#     total_attempts = TestAttempt.objects.filter(mock_test=mock_test, status='completed').count()
#     avg_score = TestAttempt.objects.filter(
#         mock_test=mock_test,
#         status='completed'
#     ).aggregate(avg=Avg('percentage'))['avg'] or 0

#     context = {
#         'mock_test': mock_test,
#         'previous_attempt': previous_attempt,
#         'total_attempts': total_attempts,
#         'average_score': round(avg_score, 2),
#     }
#     return render(request, 'mocktests/detail.html', context)
# Add these new functions to your views.py


def mock_test_detail(request, slug):
    """Show details of a specific mock test"""
    mock_test = get_object_or_404(MockTest, slug=slug, is_active=True)

    # REMOVE THIS REDIRECT BLOCK - IT'S CAUSING YOUR ISSUE
    # if mock_test.is_paid and mock_test.price > 0:
    #     if not request.user.is_authenticated:
    #         messages.warning(request, f'Please login to access "{mock_test.name}"')
    #         return redirect('accounts:login_signup')
    #
    #     if not has_payment_access(request.user, 'mock_test', mock_test.id):
    #         messages.info(request, f'Please complete payment to access "{mock_test.name}"')
    #         return redirect('payments:payment_page', item_type='mock_test', item_id=mock_test.id)

    # Check if user has purchased this test
    has_purchased = False
    if request.user.is_authenticated:
        from apps.payments.views import has_payment_access

        has_purchased = has_payment_access(request.user, "mock_test", mock_test.id)

    # Check if user has already attempted
    previous_attempt = None
    if request.user.is_authenticated:
        previous_attempt = TestAttempt.objects.filter(
            user=request.user, mock_test=mock_test, status="completed"
        ).first()

    # Get statistics
    total_attempts = TestAttempt.objects.filter(
        mock_test=mock_test, status="completed"
    ).count()
    avg_score = (
        TestAttempt.objects.filter(mock_test=mock_test, status="completed").aggregate(
            avg=Avg("percentage")
        )["avg"]
        or 0
    )

    context = {
        "mock_test": mock_test,
        "previous_attempt": previous_attempt,
        "total_attempts": total_attempts,
        "average_score": round(avg_score, 2),
        "has_purchased": has_purchased,
    }
    return render(request, "mocktests/detail.html", context)


def start_test(request, slug):
    """Start a mock test"""
    mock_test = get_object_or_404(MockTest, slug=slug, is_active=True)

    # FOR FREE TESTS - Allow without login
    if not mock_test.is_paid or mock_test.price == 0:
        # Free test - create a temporary session user or allow anonymous
        # Create a session-based attempt without requiring login
        if not request.user.is_authenticated:
            # For free tests, we'll still need an attempt record
            # Create a temporary user in session or just proceed
            # Option 1: Create a guest session
            if not request.session.get("guest_user_id"):
                request.session["guest_user_id"] = str(uuid.uuid4())

            # Get or create guest attempt
            guest_id = request.session.get("guest_user_id")
            attempt = TestAttempt.objects.filter(
                session_id=guest_id, mock_test=mock_test, status="in_progress"
            ).first()

            if not attempt:
                end_time = timezone.now() + timezone.timedelta(
                    minutes=mock_test.duration_minutes
                )
                attempt = TestAttempt.objects.create(
                    user=None,  # Anonymous user
                    session_id=guest_id,
                    mock_test=mock_test,
                    start_time=timezone.now(),
                    end_time=end_time,
                    status="in_progress",
                )
        else:
            # Logged in user for free test
            attempt = TestAttempt.objects.filter(
                user=request.user, mock_test=mock_test, status="in_progress"
            ).first()

            if not attempt:
                end_time = timezone.now() + timezone.timedelta(
                    minutes=mock_test.duration_minutes
                )
                attempt = TestAttempt.objects.create(
                    user=request.user,
                    mock_test=mock_test,
                    start_time=timezone.now(),
                    end_time=end_time,
                    status="in_progress",
                )
    else:
        # PAID TEST - Login required
        if not request.user.is_authenticated:
            messages.warning(request, f'Please login to access "{mock_test.name}"')
            return redirect("accounts:login_signup")

        # Check payment access
        if not has_payment_access(request.user, "mock_test", mock_test.id):
            messages.info(
                request, f'Please complete payment to access "{mock_test.name}"'
            )
            return redirect(
                "payments:payment_page", item_type="mock_test", item_id=mock_test.id
            )

        # Check existing attempt
        attempt = TestAttempt.objects.filter(
            user=request.user, mock_test=mock_test, status="in_progress"
        ).first()

        if not attempt:
            end_time = timezone.now() + timezone.timedelta(
                minutes=mock_test.duration_minutes
            )
            attempt = TestAttempt.objects.create(
                user=request.user,
                mock_test=mock_test,
                start_time=timezone.now(),
                end_time=end_time,
                status="in_progress",
            )

    # Get questions (same for both)
    mock_test_questions = mock_test.get_questions()

    # Prepare questions data
    questions_data = []
    for mtq in mock_test_questions:
        question = mtq.question
        options = list(question.options.values("id", "option_text", "order"))

        if mock_test.shuffle_options:
            random.shuffle(options)

        questions_data.append(
            {
                "id": question.id,
                "text": question.question_text,
                "type": question.question_type,
                "marks": mtq.marks,
                "negative_marks": question.negative_marks,
                "options": options,
            }
        )

    context = {
        "attempt": attempt,
        "mock_test": mock_test,
        "questions": questions_data,
        "total_questions": len(questions_data),
        "end_time": int(attempt.end_time.timestamp() * 1000),
    }
    return render(request, "mocktests/test_window.html", context)


# @login_required
# def start_test(request, slug):
#     """Start a mock test"""
#     mock_test = get_object_or_404(MockTest, slug=slug, is_active=True)

#     # Check if user has reached max attempts
#     attempts_count = TestAttempt.objects.filter(
#         user=request.user,
#         mock_test=mock_test,
#         status='completed'
#     ).count()

#     # Allow unlimited attempts for now
#     # # if attempts_count >= mock_test.attempts_allowed:
#     # if mock_test.attempts_allowed > 0 and attempts_count >= mock_test.attempts_allowed:
#     #     messages.error(request, f'You have reached the maximum allowed attempts ({mock_test.attempts_allowed}) for this test.')
#     #     return redirect('mocktests:detail', slug=mock_test.slug)

#     # Check for existing in-progress attempt
#     attempt = TestAttempt.objects.filter(
#         user=request.user,
#         mock_test=mock_test,
#         status='in_progress'
#     ).first()

#     if not attempt:
#         # Create new attempt
#         end_time = timezone.now() + timezone.timedelta(minutes=mock_test.duration_minutes)
#         attempt = TestAttempt.objects.create(
#             user=request.user,
#             mock_test=mock_test,
#             start_time=timezone.now(),
#             end_time=end_time,
#             status='in_progress'
#         )

#     # Get questions
#     mock_test_questions = mock_test.get_questions()

#     # Prepare questions data
#     questions_data = []
#     for mtq in mock_test_questions:
#         question = mtq.question
#         options = list(question.options.values('id', 'option_text', 'order'))

#         if mock_test.shuffle_options:
#             random.shuffle(options)

#         questions_data.append({
#             'id': question.id,
#             'text': question.question_text,
#             'type': question.question_type,
#             'marks': mtq.marks,
#             'negative_marks': question.negative_marks,
#             'options': options,
#         })

#     context = {
#         'attempt': attempt,
#         'mock_test': mock_test,
#         'questions': questions_data,
#         'total_questions': len(questions_data),
#         'end_time': int(attempt.end_time.timestamp() * 1000),
#     }
#     return render(request, 'mocktests/test_window.html', context)


@login_required
def take_mock_test(request, test_id):
    """Alternative view for starting a test by ID (for compatibility with exam buttons)"""
    mock_test = get_object_or_404(MockTest, id=test_id, is_active=True)
    return start_test(request, slug=mock_test.slug)


@csrf_exempt
def save_answer(request):
    """Save answer via AJAX"""
    if request.method == "POST":

        try:
            data = json.loads(request.body)
            attempt_id = data.get("attempt_id")
            question_id = data.get("question_id")
            selected_option = data.get("selected_option")
            time_taken = data.get("time_taken", 0)

            # attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
            attempt = get_object_or_404(TestAttempt, id=attempt_id)

            # Verify access
            if attempt.user is None:
                guest_id = request.session.get("guest_user_id")
                if attempt.session_id != guest_id:
                    return JsonResponse(
                        {"success": False, "error": "Unauthorized"}, status=403
                    )
            else:
                if attempt.user != request.user:
                    return JsonResponse(
                        {"success": False, "error": "Unauthorized"}, status=403
                    )

            question = get_object_or_404(Question, id=question_id)

            # Get the mock test question to get marks
            mtq = MockTestQuestion.objects.get(
                mock_test=attempt.mock_test, question=question
            )

            # Calculate if correct
            is_correct = False
            marks_obtained = 0

            if selected_option:
                option = question.options.filter(
                    id=selected_option, is_correct=True
                ).first()
                if option:
                    is_correct = True
                    marks_obtained = mtq.marks
                else:
                    marks_obtained = (
                        -question.negative_marks
                        if attempt.mock_test.negative_marking
                        else 0
                    )

            # Save answer
            answer, created = TestAnswer.objects.update_or_create(
                attempt=attempt,
                question=question,
                defaults={
                    "selected_option": selected_option,
                    "is_correct": is_correct,
                    "marks_obtained": marks_obtained,
                    "time_taken": time_taken,
                    "is_skipped": False,
                    "answered_at": timezone.now(),
                },
            )

            return JsonResponse(
                {
                    "success": True,
                    "is_correct": is_correct,
                    "marks_obtained": marks_obtained,
                }
            )

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


# @login_required
def save_answer_ajax(request, attempt_id):
    """Alternative save answer endpoint (for compatibility)"""
    return save_answer(request)


def submit_test(request, attempt_id):
    """Submit the complete test with marked for review support"""
    attempt = get_object_or_404(TestAttempt, id=attempt_id)

    # Check authorization
    is_authorized = False
    is_guest = False

    if request.user.is_authenticated:
        if attempt.user == request.user:
            is_authorized = True
    else:
        guest_id = request.session.get("guest_user_id")
        if attempt.session_id and attempt.session_id == guest_id:
            is_authorized = True
            is_guest = True

    if not is_authorized:
        messages.error(request, "You are not authorized to submit this test.")
        return redirect("home")

    if request.method == "POST":
        # Get all questions from the mock test
        mock_test_questions = MockTestQuestion.objects.filter(
            mock_test=attempt.mock_test
        )
        all_question_ids = set(
            mock_test_questions.values_list("question_id", flat=True)
        )

        # Delete existing answers (clean slate)
        TestAnswer.objects.filter(attempt=attempt).delete()

        # Track answered and marked questions
        answered_question_ids = set()
        marked_question_ids = set()

        # Save answers from POST data
        for key, value in request.POST.items():
            if key.startswith("question_"):
                question_id = key.replace("question_", "")
                selected_option = value

                if question_id and selected_option:
                    answered_question_ids.add(int(question_id))
                    try:
                        question = Question.objects.get(id=question_id)
                        option = Option.objects.get(id=selected_option)

                        is_correct = option.is_correct
                        marks_obtained = (
                            question.marks if is_correct else -question.negative_marks
                        )

                        # Check if this question was marked for review
                        is_marked = request.POST.get(f"marked_{question_id}") == "true"
                        if is_marked:
                            marked_question_ids.add(int(question_id))

                        # IMPORTANT: If answered, it's NOT skipped even if marked
                        is_skipped = False  # Answered questions are never skipped

                        TestAnswer.objects.create(
                            attempt=attempt,
                            question=question,
                            selected_option=selected_option,
                            is_correct=is_correct,
                            marks_obtained=marks_obtained,
                            time_taken=0,
                            is_skipped=is_skipped,  # Always False for answered
                            is_marked_for_review=is_marked,
                            answered_at=timezone.now(),
                        )
                    except (Question.DoesNotExist, Option.DoesNotExist):
                        pass

        # Now handle questions that were marked but NOT answered
        for question_id in all_question_ids:
            if question_id not in answered_question_ids:
                # Check if this question was marked for review
                is_marked = request.POST.get(f"marked_{question_id}") == "true"
                if is_marked:
                    # Create a skipped entry for marked but unanswered questions
                    question = Question.objects.get(id=question_id)
                    TestAnswer.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_option=None,
                        is_correct=False,
                        marks_obtained=0,
                        time_taken=0,
                        is_skipped=True,  # Marked but unanswered = skipped
                        is_marked_for_review=True,
                        answered_at=timezone.now(),
                    )

        # Calculate stats
        answers = TestAnswer.objects.filter(attempt=attempt)
        total_questions = len(all_question_ids)

        total_score = 0
        correct_count = 0
        wrong_count = 0
        skipped_count = 0
        marked_count = 0

        for answer in answers:
            total_score += answer.marks_obtained
            if answer.is_correct:
                correct_count += 1
            else:
                wrong_count += 1
            if answer.is_skipped:
                skipped_count += 1
            if answer.is_marked_for_review:
                marked_count += 1

        # Calculate counts
        answered_count = len(answered_question_ids)
        not_answered_count = total_questions - answered_count - skipped_count

        # Update attempt
        attempt.score = total_score
        attempt.percentage = (
            (total_score / attempt.mock_test.total_marks) * 100
            if attempt.mock_test.total_marks > 0
            else 0
        )
        attempt.correct_answers = correct_count
        attempt.wrong_answers = wrong_count
        attempt.skipped_answers = skipped_count  # Only marked but unanswered
        attempt.not_answered_count = not_answered_count
        attempt.total_questions = total_questions
        attempt.status = "completed"
        attempt.end_time = timezone.now()
        attempt.save()

        print(f"=== SUBMIT DEBUG ===")
        print(f"Total Questions: {total_questions}")
        print(f"Answered: {answered_count}")
        print(f"Correct: {correct_count}")
        print(f"Wrong: {wrong_count}")
        print(f"Skipped (Marked but Unanswered): {skipped_count}")
        print(f"Not Answered: {not_answered_count}")
        print(f"Total Score: {total_score}")
        print(f"Percentage: {attempt.percentage}")

        return redirect("mocktests:results", attempt_id=attempt.id)

    return redirect("mocktests:detail", slug=attempt.mock_test.slug)


# @login_required
def submit_mock_test(request, attempt_id):
    """Alternative submit endpoint (for compatibility)"""
    return submit_test(request, attempt_id)


def test_results(request, attempt_id):
    """Show test results with detailed analysis including marked for review"""
    attempt = get_object_or_404(TestAttempt, id=attempt_id)

    # Check authorization
    is_authorized = False
    is_guest = False

    if request.user.is_authenticated:
        if attempt.user == request.user:
            is_authorized = True
    else:
        guest_id = request.session.get("guest_user_id")
        if attempt.session_id and attempt.session_id == guest_id:
            is_authorized = True
            is_guest = True

    if not is_authorized:
        messages.error(request, "You are not authorized to view these results.")
        return redirect("home")

    # Get all questions from the mock test
    mock_test_questions = MockTestQuestion.objects.filter(
        mock_test=attempt.mock_test
    ).select_related("question")
    all_question_ids = set(mock_test_questions.values_list("question_id", flat=True))
    total_questions = len(all_question_ids)

    # Get user's answers
    answers = TestAnswer.objects.filter(attempt=attempt).select_related(
        "question", "question__subject", "question__topic"
    )
    answered_question_ids = set(answers.values_list("question_id", flat=True))

    # Build question analysis for ALL questions
    question_analysis = []

    # Process answered questions
    for answer in answers:
        question = answer.question
        correct_option = question.options.filter(is_correct=True).first()

        user_answer_text = None
        if answer.selected_option:
            selected_opt = question.options.filter(id=answer.selected_option).first()
            user_answer_text = (
                selected_opt.option_text if selected_opt else answer.selected_option
            )

        # Determine status
        if answer.is_skipped:
            status = "marked_for_review_skipped"  # Marked but unanswered
        elif answer.is_marked_for_review and not answer.is_skipped:
            status = "marked_for_review_answered"  # Marked and answered
        elif answer.is_correct:
            status = "correct"
        else:
            status = "wrong"

        question_analysis.append(
            {
                "question": question,
                "answer": answer,
                "correct_option": correct_option,
                "user_answer": answer.selected_option,
                "user_answer_text": user_answer_text,
                "is_correct": answer.is_correct,
                "is_skipped": answer.is_skipped,
                "is_marked_for_review": answer.is_marked_for_review,
                "status": status,
                "not_answered": False,
                "time_taken": answer.time_taken,
                "marks_obtained": answer.marks_obtained,
            }
        )

    # Process not answered questions
    for mtq in mock_test_questions:
        question = mtq.question
        if question.id not in answered_question_ids:
            correct_option = question.options.filter(is_correct=True).first()
            question_analysis.append(
                {
                    "question": question,
                    "answer": None,
                    "correct_option": correct_option,
                    "user_answer": None,
                    "user_answer_text": None,
                    "is_correct": False,
                    "is_skipped": False,
                    "is_marked_for_review": False,
                    "status": "not_answered",
                    "not_answered": True,
                    "time_taken": 0,
                    "marks_obtained": 0,
                }
            )

    # Calculate statistics
    attempted_count = len(answered_question_ids)
    not_answered_count = total_questions - attempted_count
    correct_count = answers.filter(is_correct=True, is_skipped=False).count()
    wrong_count = answers.filter(is_correct=False, is_skipped=False).count()
    skipped_count = answers.filter(is_skipped=True).count()  # Marked but unanswered
    marked_answered_count = answers.filter(
        is_marked_for_review=True, is_skipped=False
    ).count()  # Marked and answered

    # Calculate accuracy
    attempted_non_skipped = attempted_count - skipped_count
    accuracy_on_attempted = (
        (correct_count / attempted_non_skipped * 100)
        if attempted_non_skipped > 0
        else 0
    )

    # Calculate section-wise performance
    section_stats = {}
    for answer in answers:
        if answer.is_skipped:
            continue
        subject_name = (
            answer.question.subject.name if answer.question.subject else "General"
        )
        if subject_name not in section_stats:
            section_stats[subject_name] = {"correct": 0, "attempted": 0, "accuracy": 0}

        section_stats[subject_name]["attempted"] += 1
        if answer.is_correct:
            section_stats[subject_name]["correct"] += 1
        if section_stats[subject_name]["attempted"] > 0:
            section_stats[subject_name]["accuracy"] = (
                section_stats[subject_name]["correct"]
                / section_stats[subject_name]["attempted"]
            ) * 100

    context = {
        "attempt": attempt,
        "question_analysis": question_analysis,
        "section_stats": section_stats,
        "total_questions": total_questions,
        "attempted_count": attempted_count,
        "not_answered_count": not_answered_count,
        "correct_count": correct_count,
        "wrong_count": wrong_count,
        "skipped_count": skipped_count,  # Marked but unanswered
        "marked_answered_count": marked_answered_count,  # Marked and answered
        "accuracy_on_attempted": accuracy_on_attempted,
        "time_taken_minutes": (
            attempt.total_time_taken // 60 if attempt.total_time_taken else 0
        ),
        "time_taken_seconds": (
            attempt.total_time_taken % 60 if attempt.total_time_taken else 0
        ),
    }
    return render(request, "mocktests/results.html", context)


def test_result(request, attempt_id):
    """Alternative results endpoint (for compatibility)"""
    return test_results(request, attempt_id)


def get_question_data(request, attempt_id, question_id):
    """Get question data for AJAX loading"""
    attempt = get_object_or_404(TestAttempt, id=attempt_id)

    # Check authorization
    if request.user.is_authenticated:
        if attempt.user != request.user:
            return JsonResponse({"error": "Unauthorized"}, status=403)
    else:
        guest_id = request.session.get("guest_user_id")
        if attempt.session_id != guest_id:
            return JsonResponse({"error": "Unauthorized"}, status=403)

    question = get_object_or_404(Question, id=question_id)

    # Get user's answer for this question if exists
    user_answer = TestAnswer.objects.filter(attempt=attempt, question=question).first()

    # Get mock test question details
    mtq = MockTestQuestion.objects.filter(
        mock_test=attempt.mock_test, question=question
    ).first()

    options_data = []
    for option in question.options.all().order_by("order"):
        options_data.append(
            {
                "id": option.id,
                "text": option.option_text,
                "is_selected": user_answer
                and user_answer.selected_option == str(option.id),
            }
        )

    data = {
        "id": question.id,
        "text": question.question_text,
        "question_type": question.question_type,
        "marks": mtq.marks if mtq else question.marks,
        "negative_marks": question.negative_marks,
        "options": options_data,
        "has_answer": user_answer is not None,
        "selected_option": user_answer.selected_option if user_answer else None,
    }

    return JsonResponse(data)
