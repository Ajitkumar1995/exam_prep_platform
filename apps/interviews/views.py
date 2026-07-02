from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.utils import timezone
from apps.cache.decorators import anonymous_cache_page
from apps.cache.timeouts import CacheTimeout
import json
import re
from .models import InterviewCategory, InterviewQuestion, UserInterviewProgress


@anonymous_cache_page(CacheTimeout.STUDY_MATERIAL, key_prefix="interview_home")
def interview_home(request):
    """Interview preparation home page"""
    categories = InterviewCategory.objects.filter(is_active=True)

    # Get featured questions (most recent)
    featured_questions = InterviewQuestion.objects.filter(is_active=True).order_by(
        "-created_at"
    )[:6]

    # Get user progress if logged in
    total_questions = InterviewQuestion.objects.filter(is_active=True).count()
    completed_count = 0
    recent_practice = []

    if request.user.is_authenticated:
        completed_count = UserInterviewProgress.objects.filter(
            user=request.user, is_completed=True
        ).count()

        recent_practice = (
            UserInterviewProgress.objects.filter(user=request.user, is_completed=True)
            .select_related("question")
            .order_by("-attempted_at")[:5]
        )

    # Calculate category-wise question counts
    category_counts = {}
    for category in categories:
        category_counts[category.id] = InterviewQuestion.objects.filter(
            category=category, is_active=True
        ).count()

    context = {
        "categories": categories,
        "featured_questions": featured_questions,
        "total_questions": total_questions,
        "completed_count": completed_count,
        "completion_percentage": (
            (completed_count / total_questions * 100) if total_questions > 0 else 0
        ),
        "recent_practice": recent_practice,
        "category_counts": category_counts,  # This is a dictionary
    }
    return render(request, "interviews/home.html", context)


@anonymous_cache_page(CacheTimeout.STUDY_MATERIAL, key_prefix="question_bank")
def question_bank(request):
    """Browse all interview questions with filters"""
    questions = InterviewQuestion.objects.filter(is_active=True).select_related(
        "category"
    )

    # Filter by category
    category_slug = request.GET.get("category")
    if category_slug:
        questions = questions.filter(category__slug=category_slug)

    # Filter by question type
    question_type = request.GET.get("type")
    if question_type:
        questions = questions.filter(question_type=question_type)

    # Filter by difficulty
    difficulty = request.GET.get("difficulty")
    if difficulty:
        questions = questions.filter(difficulty=difficulty)

    # Search
    search_query = request.GET.get("q")
    if search_query:
        questions = questions.filter(
            Q(question_text__icontains=search_query)
            | Q(keywords__icontains=search_query)
        )

    paginator = Paginator(questions, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = InterviewCategory.objects.filter(is_active=True)

    # Get user's answered questions
    answered_questions = []
    if request.user.is_authenticated:
        answered_questions = UserInterviewProgress.objects.filter(
            user=request.user, is_completed=True
        ).values_list("question_id", flat=True)

    context = {
        "questions": page_obj,
        "categories": categories,
        "answered_questions": list(answered_questions),
        "selected_category": category_slug,
        "selected_type": question_type,
        "selected_difficulty": difficulty,
        "search_query": search_query,
    }
    return render(request, "interviews/question_bank.html", context)


@login_required
def practice_question(request, pk):
    """Practice a specific interview question"""
    question = get_object_or_404(InterviewQuestion, pk=pk, is_active=True)

    # Get user's previous answer if any
    user_progress = UserInterviewProgress.objects.filter(
        user=request.user, question=question
    ).first()

    # Get next and previous questions
    all_questions = InterviewQuestion.objects.filter(is_active=True).values_list(
        "id", flat=True
    )

    question_ids = list(all_questions)
    current_index = (
        question_ids.index(question.id) if question.id in question_ids else -1
    )

    next_question = None
    prev_question = None

    if current_index != -1:
        if current_index + 1 < len(question_ids):
            next_question = InterviewQuestion.objects.get(
                id=question_ids[current_index + 1]
            )
        if current_index - 1 >= 0:
            prev_question = InterviewQuestion.objects.get(
                id=question_ids[current_index - 1]
            )

    # Get similar questions (same category)
    similar_questions = InterviewQuestion.objects.filter(
        category=question.category, is_active=True
    ).exclude(id=question.id)[:3]

    context = {
        "question": question,
        "user_progress": user_progress,
        "next_question": next_question,
        "prev_question": prev_question,
        "similar_questions": similar_questions,
    }
    return render(request, "interviews/practice.html", context)


@login_required
def submit_answer(request):
    """Submit answer for a question and get AI evaluation"""
    if request.method == "POST":
        data = json.loads(request.body)
        question_id = data.get("question_id")
        user_answer = data.get("answer")
        time_taken = data.get("time_taken", 0)

        question = get_object_or_404(InterviewQuestion, id=question_id)

        # Evaluate answer
        evaluation = evaluate_answer(user_answer, question)

        # Save progress
        progress, created = UserInterviewProgress.objects.update_or_create(
            user=request.user,
            question=question,
            defaults={
                "user_answer": user_answer,
                "score": evaluation["score"],
                "feedback": evaluation["feedback"],
                "is_completed": True,
                "updated_at": timezone.now(),
            },
        )

        return JsonResponse(
            {
                "success": True,
                "score": evaluation["score"],
                "rating": evaluation["rating"],
                "feedback": evaluation["feedback"],
                "strengths": evaluation.get("strengths", []),
                "improvements": evaluation.get("improvements", []),
                "sample_answer": question.sample_answer,
                "tips": question.tips,
                "word_count": evaluation.get("word_count", 0),
                "keywords_found": evaluation.get("keywords_found", 0),
                "total_keywords": evaluation.get("total_keywords", 0),
            }
        )

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def evaluate_answer(user_answer, question):
    """AI-powered evaluation of user's answer based on question keywords"""
    user_answer_lower = user_answer.lower()
    user_answer_words = set(re.findall(r"\w+", user_answer_lower))

    # Extract keywords from question
    keywords = (
        [kw.strip().lower() for kw in question.keywords.split(",")]
        if question.keywords
        else []
    )

    # Calculate keyword match score
    matched_keywords = []
    for kw in keywords:
        if kw in user_answer_lower:
            matched_keywords.append(kw)

    keyword_score = (len(matched_keywords) / len(keywords) * 100) if keywords else 70

    # Calculate length score (ideal: 100-300 words)
    word_count = len(user_answer.split())
    if word_count < 50:
        length_score = max(0, (word_count / 50) * 50)
    elif word_count > 500:
        length_score = 80
    else:
        length_score = 100

    # Calculate structure score
    sentences = [s.strip() for s in user_answer.split(".") if s.strip()]
    paragraphs = user_answer.split("\n\n")

    structure_score = 70
    if len(sentences) >= 3:
        structure_score += 10
    if len(paragraphs) >= 2:
        structure_score += 10
    if any(
        word in user_answer_lower
        for word in ["first", "second", "third", "finally", "moreover"]
    ):
        structure_score += 10

    structure_score = min(100, structure_score)

    # Calculate overall score
    overall_score = (
        (keyword_score * 0.5) + (length_score * 0.3) + (structure_score * 0.2)
    )
    overall_score = min(100, max(0, overall_score))

    # Generate rating and feedback
    if overall_score >= 85:
        rating = "Excellent"
        feedback = "Excellent answer! You've covered key points effectively and demonstrated strong understanding."
    elif overall_score >= 70:
        rating = "Good"
        feedback = "Good answer! You've addressed most key points. Consider adding more specific examples."
    elif overall_score >= 50:
        rating = "Average"
        feedback = "Satisfactory answer. Try to be more thorough and include all key points with examples."
    else:
        rating = "Needs Improvement"
        feedback = "Your answer needs improvement. Review the sample answer and focus on key areas."

    # Generate strengths
    strengths = []
    if keyword_score > 70:
        strengths.append(f"Good use of keywords: {', '.join(matched_keywords[:3])}")
    if word_count > 100:
        strengths.append("Excellent length - detailed and comprehensive answer")
    if len(sentences) > 3:
        strengths.append("Good structure with multiple paragraphs")
    if structure_score > 80:
        strengths.append("Well-organized answer with clear flow")

    # Generate improvement areas
    improvements = []
    missing_keywords = [kw for kw in keywords if kw not in matched_keywords][:3]
    if missing_keywords:
        improvements.append(f"Consider including: {', '.join(missing_keywords)}")
    if word_count < 80:
        improvements.append(
            "Elaborate more on your points - provide more details and examples"
        )
    if len(sentences) < 2:
        improvements.append(
            "Break down your answer into multiple sentences or paragraphs"
        )
    if keyword_score < 50:
        improvements.append("Use more relevant keywords from the question")

    return {
        "score": round(overall_score, 1),
        "rating": rating,
        "feedback": feedback,
        "strengths": strengths[:3],
        "improvements": improvements[:3],
        "keywords_found": len(matched_keywords),
        "total_keywords": len(keywords),
        "word_count": word_count,
    }


@login_required
def mock_interview(request):
    """AI-powered mock interview simulation"""
    # Get random questions for mock interview
    questions = InterviewQuestion.objects.filter(is_active=True).order_by("?")[:10]

    if request.method == "POST":
        # Process submitted answers
        answers_data = json.loads(request.POST.get("answers", "{}"))
        results = []
        total_score = 0

        for question_id, answer in answers_data.items():
            question = InterviewQuestion.objects.get(id=question_id)
            evaluation = evaluate_answer(answer, question)
            total_score += evaluation["score"]
            results.append(
                {"question": question, "answer": answer, "evaluation": evaluation}
            )

        avg_score = total_score / len(questions) if questions else 0

        context = {
            "results": results,
            "avg_score": avg_score,
            "total_questions": len(questions),
        }
        return render(request, "interviews/mock_results.html", context)

    context = {
        "questions": questions,
        "total_questions": questions.count(),
    }
    return render(request, "interviews/mock_interview.html", context)


@login_required
def interview_tips(request):
    """Interview tips and guidance (admin can add tips via admin panel)"""
    # Get tips from all categories (you can expand this as needed)
    context = {
        "tips_categories": [],  # Empty - admin should add content via admin panel
    }
    return render(request, "interviews/tips.html", context)


@login_required
def my_progress(request):
    """View user's interview preparation progress"""
    progress = (
        UserInterviewProgress.objects.filter(user=request.user, is_completed=True)
        .select_related("question", "question__category")
        .order_by("-attempted_at")
    )

    # Calculate statistics
    total_attempted = progress.count()
    average_score = progress.aggregate(avg=Avg("score"))["avg"] or 0

    # Category breakdown
    category_breakdown = {}
    for p in progress:
        cat_name = p.question.category.name
        if cat_name not in category_breakdown:
            category_breakdown[cat_name] = {"count": 0, "total_score": 0}
        category_breakdown[cat_name]["count"] += 1
        category_breakdown[cat_name]["total_score"] += p.score

    for cat in category_breakdown:
        category_breakdown[cat]["avg_score"] = (
            category_breakdown[cat]["total_score"] / category_breakdown[cat]["count"]
        )

    # Difficulty breakdown
    difficulty_breakdown = {}
    for p in progress:
        difficulty = p.question.difficulty
        if difficulty not in difficulty_breakdown:
            difficulty_breakdown[difficulty] = {"count": 0, "total_score": 0}
        difficulty_breakdown[difficulty]["count"] += 1
        difficulty_breakdown[difficulty]["total_score"] += p.score

    for diff in difficulty_breakdown:
        difficulty_breakdown[diff]["avg_score"] = (
            difficulty_breakdown[diff]["total_score"]
            / difficulty_breakdown[diff]["count"]
        )

    paginator = Paginator(progress, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "progress": page_obj,
        "total_attempted": total_attempted,
        "average_score": round(average_score, 1),
        "category_breakdown": category_breakdown,
        "difficulty_breakdown": difficulty_breakdown,
    }
    return render(request, "interviews/progress.html", context)


@anonymous_cache_page(CacheTimeout.STUDY_MATERIAL, key_prefix="category_questions")
def category_questions(request, slug):
    """View questions by category"""
    category = get_object_or_404(InterviewCategory, slug=slug, is_active=True)
    questions = InterviewQuestion.objects.filter(category=category, is_active=True)

    # Get user's answered questions
    answered_questions = []
    if request.user.is_authenticated:
        answered_questions = UserInterviewProgress.objects.filter(
            user=request.user, is_completed=True
        ).values_list("question_id", flat=True)

    paginator = Paginator(questions, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "category": category,
        "questions": page_obj,
        "answered_questions": list(answered_questions),
    }
    return render(request, "interviews/category_questions.html", context)


@login_required
def save_progress(request):
    """Save practice progress (AJAX)"""
    if request.method == "POST":
        data = json.loads(request.body)
        question_id = data.get("question_id")
        is_completed = data.get("is_completed", True)

        question = get_object_or_404(InterviewQuestion, id=question_id)

        progress, created = UserInterviewProgress.objects.get_or_create(
            user=request.user, question=question
        )

        if is_completed and not progress.is_completed:
            progress.is_completed = True
            progress.save()
            return JsonResponse({"success": True, "message": "Progress saved"})

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)
