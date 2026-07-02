from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Count, Avg, Q
from django.core.paginator import Paginator
from .models import MockTest, TestAttempt, TestAnswer, MockTestQuestion
from apps.exams.models import Question, Option
from apps.payments.views import has_payment_access
import json
import random
import uuid
from apps.cache.decorators import anonymous_cache_page
from apps.cache.timeouts import CacheTimeout


def _is_attempt_authorized(request, attempt):
    """Return whether the request user/session can access an attempt."""
    if request.user.is_authenticated:
        return attempt.user == request.user
    guest_id = request.session.get("guest_user_id")
    return bool(attempt.session_id and attempt.session_id == guest_id)


def add_to_cart_redirect(request, mock_test_id):
    """Redirect mock test cart additions to the shared payment cart."""
    return redirect("payments:add_to_cart", item_type="mock_test", item_id=mock_test_id)


@anonymous_cache_page(CacheTimeout.MOCK_TEST_LIST, key_prefix="mock_test_list")
def mock_test_list(request):
    """Render the searchable, paginated list of active mock tests."""
    mock_tests = MockTest.objects.filter(is_active=True).select_related("exam")

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

    for test in page_obj:
        test.is_free = not test.is_paid or test.price == 0

    context = {
        "mock_tests": page_obj,
        "search_query": search_query,
    }
    return render(request, "mocktests/list.html", context)


@anonymous_cache_page(CacheTimeout.MOCK_TEST_DETAIL, key_prefix="mock_test_detail")
def mock_test_detail(request, slug):
    """Render one active mock test with attempt stats and purchase state."""
    mock_test = get_object_or_404(
        MockTest.objects.select_related("exam", "subject", "topic"),
        slug=slug,
        is_active=True,
    )

    has_purchased = False
    if request.user.is_authenticated:
        has_purchased = has_payment_access(request.user, "mock_test", mock_test.id)

    previous_attempt = None
    if request.user.is_authenticated:
        previous_attempt = TestAttempt.objects.filter(
            user=request.user, mock_test=mock_test, status="completed"
        ).first()

    stats = TestAttempt.objects.filter(
        mock_test=mock_test, status="completed"
    ).aggregate(
        total_attempts=Count("id"),
        average_score=Avg("percentage"),
    )

    context = {
        "mock_test": mock_test,
        "previous_attempt": previous_attempt,
        "total_attempts": stats["total_attempts"] or 0,
        "average_score": round(stats["average_score"] or 0, 2),
        "has_purchased": has_purchased,
    }
    return render(request, "mocktests/detail.html", context)


def start_test(request, slug):
    """Create or resume an authorized attempt and render the test window."""
    mock_test = get_object_or_404(
        MockTest.objects.select_related("exam", "subject", "topic"),
        slug=slug,
        is_active=True,
    )

    if not mock_test.is_paid or mock_test.price == 0:
        if not request.user.is_authenticated:
            if not request.session.get("guest_user_id"):
                request.session["guest_user_id"] = str(uuid.uuid4())

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
        if not request.user.is_authenticated:
            messages.warning(request, f'Please login to access "{mock_test.name}"')
            return redirect("accounts:login_signup")

        if not has_payment_access(request.user, "mock_test", mock_test.id):
            messages.info(
                request, f'Please complete payment to access "{mock_test.name}"'
            )
            return redirect(
                "payments:payment_page", item_type="mock_test", item_id=mock_test.id
            )

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

    mock_test_questions = mock_test.get_questions()

    questions_data = []
    for mtq in mock_test_questions:
        question = mtq.question
        options = [
            {
                "id": option.id,
                "option_text": option.option_text,
                "order": option.order,
            }
            for option in question.options.all()
        ]

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


@login_required
def take_mock_test(request, test_id):
    """Start a mock test from routes that identify the test by database ID."""
    mock_test = get_object_or_404(MockTest, id=test_id, is_active=True)
    return start_test(request, slug=mock_test.slug)


@csrf_exempt
def save_answer(request):
    """Save or update one AJAX answer after validating attempt ownership."""
    if request.method == "POST":

        try:
            data = json.loads(request.body)
            attempt_id = data.get("attempt_id")
            question_id = data.get("question_id")
            selected_option = data.get("selected_option")
            time_taken = data.get("time_taken", 0)

            # attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
            attempt = get_object_or_404(
                TestAttempt.objects.select_related("mock_test"), id=attempt_id
            )

            if not _is_attempt_authorized(request, attempt):
                return JsonResponse(
                    {"success": False, "error": "Unauthorized"}, status=403
                )

            question = get_object_or_404(
                Question.objects.only(
                    "id", "question_text", "negative_marks", "marks"
                ),
                id=question_id,
            )

            mtq = MockTestQuestion.objects.get(
                mock_test=attempt.mock_test, question=question
            )

            is_correct = False
            marks_obtained = 0

            if selected_option:
                option = Option.objects.filter(
                    id=selected_option, question_id=question_id
                ).only("is_correct").first()
                if option and option.is_correct:
                    is_correct = True
                    marks_obtained = mtq.marks
                elif option:
                    marks_obtained = (
                        -question.negative_marks
                        if attempt.mock_test.negative_marking
                        else 0
                    )
                else:
                    return JsonResponse(
                        {"success": False, "error": "Invalid option"}, status=400
                    )

            TestAnswer.objects.update_or_create(
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


def save_answer_ajax(request, attempt_id):
    """Save an answer through the legacy URL that includes attempt_id."""
    return save_answer(request)


def submit_test(request, attempt_id):
    """Finalize a test attempt and persist scored answers in bulk."""
    attempt = get_object_or_404(
        TestAttempt.objects.select_related("mock_test"), id=attempt_id
    )

    if not _is_attempt_authorized(request, attempt):
        messages.error(request, "You are not authorized to submit this test.")
        return redirect("home")

    if request.method == "POST":
        mock_test_questions = list(
            MockTestQuestion.objects.filter(mock_test=attempt.mock_test).select_related(
                "question"
            )
        )
        all_question_ids = {mtq.question_id for mtq in mock_test_questions}

        TestAnswer.objects.filter(attempt=attempt).delete()

        answered_question_ids = set()
        posted_answers = []

        for key, value in request.POST.items():
            if key.startswith("question_") and value:
                try:
                    question_id = int(key.replace("question_", ""))
                    selected_option_id = int(value)
                except (TypeError, ValueError):
                    continue
                if question_id in all_question_ids:
                    posted_answers.append((question_id, selected_option_id, value))

        question_map = {
            mtq.question_id: mtq.question for mtq in mock_test_questions
        }
        option_map = Option.objects.in_bulk(
            [option_id for _question_id, option_id, _raw in posted_answers]
        )
        answer_objects = []

        for question_id, selected_option_id, selected_option in posted_answers:
            question = question_map.get(question_id)
            option = option_map.get(selected_option_id)
            if not question or not option or option.question_id != question_id:
                continue

            answered_question_ids.add(question_id)
            is_correct = option.is_correct
            marks_obtained = question.marks if is_correct else (
                -question.negative_marks if attempt.mock_test.negative_marking else 0
            )

            is_marked = request.POST.get(f"marked_{question_id}") == "true"

            answer_objects.append(
                TestAnswer(
                    attempt=attempt,
                    question=question,
                    selected_option=selected_option,
                    is_correct=is_correct,
                    marks_obtained=marks_obtained,
                    time_taken=0,
                    is_skipped=False,
                    is_marked_for_review=is_marked,
                    answered_at=timezone.now(),
                )
            )

        for question_id in all_question_ids:
            if question_id not in answered_question_ids:
                is_marked = request.POST.get(f"marked_{question_id}") == "true"
                if is_marked:
                    question = question_map.get(question_id)
                    if not question:
                        continue
                    answer_objects.append(
                        TestAnswer(
                            attempt=attempt,
                            question=question,
                            selected_option=None,
                            is_correct=False,
                            marks_obtained=0,
                            time_taken=0,
                            is_skipped=True,
                            is_marked_for_review=True,
                            answered_at=timezone.now(),
                        )
                    )

        TestAnswer.objects.bulk_create(answer_objects)

        total_questions = len(all_question_ids)

        total_score = 0
        correct_count = 0
        wrong_count = 0
        skipped_count = 0

        for answer in answer_objects:
            total_score += answer.marks_obtained
            if answer.is_skipped:
                skipped_count += 1
            elif answer.is_correct:
                correct_count += 1
            else:
                wrong_count += 1

        answered_count = len(answered_question_ids)
        not_answered_count = total_questions - answered_count - skipped_count

        attempt.score = total_score
        attempt.percentage = (
            (total_score / attempt.mock_test.total_marks) * 100
            if attempt.mock_test.total_marks > 0
            else 0
        )
        attempt.correct_answers = correct_count
        attempt.wrong_answers = wrong_count
        attempt.skipped_answers = skipped_count
        attempt.not_answered_count = not_answered_count
        attempt.status = "completed"
        attempt.end_time = timezone.now()
        attempt.save(
            update_fields=[
                "score",
                "percentage",
                "correct_answers",
                "wrong_answers",
                "skipped_answers",
                "not_answered_count",
                "status",
                "end_time",
            ]
        )

        return redirect("mocktests:results", attempt_id=attempt.id)

    return redirect("mocktests:detail", slug=attempt.mock_test.slug)


def submit_mock_test(request, attempt_id):
    """Submit a test through the legacy alternate endpoint."""
    return submit_test(request, attempt_id)


def test_results(request, attempt_id):
    """Render result analysis for an authorized test attempt."""
    attempt = get_object_or_404(
        TestAttempt.objects.select_related("mock_test"), id=attempt_id
    )

    if not _is_attempt_authorized(request, attempt):
        messages.error(request, "You are not authorized to view these results.")
        return redirect("home")

    mock_test_questions = list(
        MockTestQuestion.objects.filter(mock_test=attempt.mock_test)
        .select_related("question")
        .prefetch_related("question__options")
    )
    all_question_ids = {mtq.question_id for mtq in mock_test_questions}
    total_questions = len(all_question_ids)

    answers = list(
        TestAnswer.objects.filter(attempt=attempt)
        .select_related("question", "question__subject", "question__topic")
        .prefetch_related("question__options")
    )
    answered_question_ids = {answer.question_id for answer in answers}

    question_analysis = []

    for answer in answers:
        question = answer.question
        options = list(question.options.all())
        correct_option = next((option for option in options if option.is_correct), None)

        user_answer_text = None
        if answer.selected_option:
            selected_opt = next(
                (
                    option
                    for option in options
                    if str(option.id) == str(answer.selected_option)
                ),
                None,
            )
            user_answer_text = (
                selected_opt.option_text if selected_opt else answer.selected_option
            )

        if answer.is_skipped:
            status = "marked_for_review_skipped"
        elif answer.is_marked_for_review and not answer.is_skipped:
            status = "marked_for_review_answered"
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

    for mtq in mock_test_questions:
        question = mtq.question
        if question.id not in answered_question_ids:
            correct_option = next(
                (option for option in question.options.all() if option.is_correct),
                None,
            )
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

    attempted_count = len(answered_question_ids)
    not_answered_count = total_questions - attempted_count
    correct_count = sum(
        1 for answer in answers if answer.is_correct and not answer.is_skipped
    )
    wrong_count = sum(
        1 for answer in answers if not answer.is_correct and not answer.is_skipped
    )
    skipped_count = sum(1 for answer in answers if answer.is_skipped)
    marked_answered_count = sum(
        1
        for answer in answers
        if answer.is_marked_for_review and not answer.is_skipped
    )

    attempted_non_skipped = attempted_count - skipped_count
    accuracy_on_attempted = (
        (correct_count / attempted_non_skipped * 100)
        if attempted_non_skipped > 0
        else 0
    )

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
        "skipped_count": skipped_count,
        "marked_answered_count": marked_answered_count,
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
    """Render results through the legacy singular endpoint."""
    return test_results(request, attempt_id)


def get_question_data(request, attempt_id, question_id):
    """Return one question payload for AJAX navigation."""
    attempt = get_object_or_404(
        TestAttempt.objects.select_related("mock_test"), id=attempt_id
    )

    if not _is_attempt_authorized(request, attempt):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    question = get_object_or_404(
        Question.objects.prefetch_related("options"), id=question_id
    )

    user_answer = TestAnswer.objects.filter(attempt=attempt, question=question).first()

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
