from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Count, Avg, Sum, Q, Max, Min
from django.utils import timezone
from datetime import timedelta, datetime
from .models import (
    UserPerformance,
    ExamPerformance,
    SubjectPerformance,
    TopicPerformance,
    DailyActivity,
)
from apps.exams.models import Exam, Subject, Topic
from apps.mocktests.models import TestAttempt, TestAnswer
import json

User = get_user_model()  # This gets your custom User model from accounts app


@login_required
def analytics_dashboard(request):
    """Main analytics dashboard with real-time data"""
    # Get or update user performance
    performance, created = UserPerformance.objects.get_or_create(user=request.user)
    performance.update_stats()

    # Get exam performances
    exam_performances = ExamPerformance.objects.filter(
        user=request.user
    ).select_related("exam")[:5]

    # Get weak and strong topics (real-time)
    weak_topics = TopicPerformance.objects.filter(
        user=request.user, is_weak=True
    ).select_related("topic__subject")[:10]

    strong_topics = TopicPerformance.objects.filter(
        user=request.user, is_strong=True
    ).select_related("topic__subject")[:10]

    # Get recent activity (last 7 days)
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    recent_activities = DailyActivity.objects.filter(
        user=request.user, date__gte=week_ago
    ).order_by("-date")

    # Get recent test attempts
    recent_attempts = (
        TestAttempt.objects.filter(user=request.user, status="completed")
        .select_related("mock_test")
        .order_by("-end_time")[:10]
    )

    # Calculate current rank and percentile
    sorted_users = list(
        User.objects.filter(test_attempts__status="completed")
        .annotate(
            avg_score=Avg(
                "test_attempts__percentage",
                filter=Q(test_attempts__status="completed"),
            )
        )
        .values_list("id", "avg_score")
        .order_by("-avg_score")
    )

    rank = None
    percentile = 0
    for idx, (user_id, _score) in enumerate(sorted_users, 1):
        if user_id == request.user.id:
            rank = idx
            percentile = (
                ((len(sorted_users) - idx) / len(sorted_users)) * 100
                if sorted_users
                else 0
            )
            break

    context = {
        "performance": performance,
        "exam_performances": exam_performances,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "recent_activities": recent_activities,
        "recent_attempts": recent_attempts,
        "rank": rank,
        "percentile": round(percentile, 1),
        "total_users": len(sorted_users),
    }
    return render(request, "analytics/dashboard.html", context)


@login_required
def exam_analytics(request, exam_slug):
    """Analytics for specific exam with real-time data"""
    exam = get_object_or_404(Exam, slug=exam_slug)

    # Get or create exam performance
    exam_perf, created = ExamPerformance.objects.get_or_create(
        user=request.user, exam=exam
    )
    exam_perf.update_stats()

    # Get subject performances for this exam (real-time)
    subject_performances = SubjectPerformance.objects.filter(
        user=request.user, subject__exam=exam
    ).select_related("subject")

    # Update subject stats
    for sp in subject_performances:
        sp.update_stats()

    # Get topic performances for this exam (real-time)
    topic_performances = TopicPerformance.objects.filter(
        user=request.user, topic__subject__exam=exam
    ).select_related("topic__subject")

    # Update topic stats
    for tp in topic_performances:
        tp.update_stats()

    # Get attempt history
    attempts = TestAttempt.objects.filter(
        user=request.user, mock_test__exam=exam, status="completed"
    ).order_by("-end_time")[:20]

    # Get attempt history for chart
    all_attempts = TestAttempt.objects.filter(
        user=request.user, mock_test__exam=exam, status="completed"
    ).order_by("end_time")

    chart_data = {
        "labels": [
            a.end_time.strftime("%b %d") if a.end_time else "N/A" for a in all_attempts
        ],
        "scores": [round(a.percentage, 1) for a in all_attempts],
        "dates": [
            a.end_time.strftime("%Y-%m-%d") if a.end_time else "" for a in all_attempts
        ],
    }

    # Calculate exam progress
    total_topics = Topic.objects.filter(subject__exam=exam).count()
    completed_topics = topic_performances.filter(is_strong=True).count()
    progress = (completed_topics / total_topics * 100) if total_topics > 0 else 0

    context = {
        "exam": exam,
        "exam_performance": exam_perf,
        "subject_performances": subject_performances,
        "topic_performances": topic_performances,
        "attempts": attempts,
        "chart_data": json.dumps(chart_data),
        "progress": round(progress, 1),
        "total_topics": total_topics,
        "completed_topics": completed_topics,
    }
    return render(request, "analytics/exam_analytics.html", context)


@login_required
def get_performance_data(request):
    """API endpoint for real-time performance data (charts)"""
    # Get all attempts
    attempts = TestAttempt.objects.filter(
        user=request.user, status="completed"
    ).order_by("end_time")

    # Prepare chart data
    chart_data = {"labels": [], "scores": [], "accuracy": [], "dates": []}

    for attempt in attempts:
        chart_data["labels"].append(attempt.mock_test.name[:20])
        chart_data["scores"].append(
            round(attempt.percentage, 1) if attempt.percentage else 0
        )
        chart_data["accuracy"].append(
            round(attempt.percentage, 1) if attempt.percentage else 0
        )
        chart_data["dates"].append(
            attempt.end_time.strftime("%b %d") if attempt.end_time else ""
        )

    # Get subject-wise performance (real-time)
    subject_perf = SubjectPerformance.objects.filter(user=request.user).select_related(
        "subject"
    )

    for sp in subject_perf:
        sp.update_stats()

    subject_data = {
        "labels": [sp.subject.name for sp in subject_perf],
        "accuracy": [round(sp.accuracy, 1) for sp in subject_perf],
        "questions": [sp.total_questions for sp in subject_perf],
    }

    # Get topic-wise weak areas (real-time)
    weak_topics = TopicPerformance.objects.filter(
        user=request.user, is_weak=True
    ).select_related("topic")[:10]

    weak_data = [
        {
            "name": wt.topic.name,
            "accuracy": round(wt.accuracy, 1),
            "questions": wt.total_questions,
        }
        for wt in weak_topics
    ]

    # Get exam-wise performance
    exam_perf = ExamPerformance.objects.filter(user=request.user).select_related("exam")

    exam_data = {
        "labels": [ep.exam.name for ep in exam_perf],
        "accuracy": [round(ep.accuracy, 1) for ep in exam_perf],
        "best_score": [round(ep.best_score, 1) for ep in exam_perf],
        "attempts": [ep.total_attempts for ep in exam_perf],
    }

    # Get daily activity for last 30 days
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    daily_activity = DailyActivity.objects.filter(
        user=request.user, date__gte=thirty_days_ago
    ).order_by("date")

    activity_data = {
        "dates": [a.date.strftime("%Y-%m-%d") for a in daily_activity],
        "questions": [a.questions_attempted for a in daily_activity],
        "time": [round(a.time_spent / 60, 1) for a in daily_activity],
    }

    # Get user performance
    performance, _ = UserPerformance.objects.get_or_create(user=request.user)
    performance.update_stats()

    return JsonResponse(
        {
            "chart_data": chart_data,
            "subject_data": subject_data,
            "weak_topics": weak_data,
            "exam_data": exam_data,
            "activity_data": activity_data,
            "total_tests": attempts.count(),
            "overall_accuracy": (
                round(performance.overall_accuracy, 1) if performance else 0
            ),
            "average_score": round(performance.average_score, 1) if performance else 0,
            "total_questions": (
                performance.total_questions_attempted if performance else 0
            ),
        }
    )


@login_required
def get_attempt_details(request, attempt_id):
    """Get detailed analysis for a specific attempt"""
    attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
    answers = TestAnswer.objects.filter(attempt=attempt).select_related(
        "question", "question__subject", "question__topic"
    )

    # Prepare question-wise breakdown
    question_analysis = []
    for answer in answers:
        question_analysis.append(
            {
                "question_text": answer.question.question_text[:100],
                "subject": (
                    answer.question.subject.name
                    if answer.question.subject
                    else "General"
                ),
                "topic": (
                    answer.question.topic.name if answer.question.topic else "General"
                ),
                "is_correct": answer.is_correct,
                "is_skipped": answer.is_skipped,
                "is_marked_for_review": answer.is_marked_for_review,
                "time_taken": answer.time_taken,
                "marks_obtained": answer.marks_obtained,
                "explanation": (
                    answer.question.explanation if answer.question.explanation else ""
                ),
            }
        )

    # Subject-wise breakdown for this attempt
    subject_breakdown = {}
    for answer in answers:
        subject = answer.question.subject.name if answer.question.subject else "General"
        if subject not in subject_breakdown:
            subject_breakdown[subject] = {
                "correct": 0,
                "wrong": 0,
                "skipped": 0,
                "total": 0,
            }

        subject_breakdown[subject]["total"] += 1
        if answer.is_correct:
            subject_breakdown[subject]["correct"] += 1
        elif answer.is_skipped:
            subject_breakdown[subject]["skipped"] += 1
        else:
            subject_breakdown[subject]["wrong"] += 1

    # Calculate percentiles for this attempt
    all_attempts = TestAttempt.objects.filter(
        mock_test=attempt.mock_test, status="completed", percentage__isnull=False
    )

    better_scores = all_attempts.filter(percentage__gt=attempt.percentage).count()
    total_attempts = all_attempts.count()
    percentile = (
        ((total_attempts - better_scores) / total_attempts * 100)
        if total_attempts > 0
        else 0
    )

    return JsonResponse(
        {
            "attempt": {
                "id": attempt.id,
                "score": attempt.score,
                "percentage": round(attempt.percentage, 1) if attempt.percentage else 0,
                "correct_answers": attempt.correct_answers,
                "wrong_answers": attempt.wrong_answers,
                "skipped_answers": attempt.skipped_answers,
                "total_questions": attempt.mock_test.total_questions,
                "rank": attempt.rank,
                "percentile": round(percentile, 1),
                "time_taken": attempt.total_time_taken,
            },
            "question_analysis": question_analysis,
            "subject_breakdown": subject_breakdown,
        }
    )


@login_required
def update_all_stats(request):
    """Manual trigger to update all user stats (real-time)"""
    # Update user performance
    performance, _ = UserPerformance.objects.get_or_create(user=request.user)
    performance.update_stats()

    # Update exam performances
    exams = Exam.objects.filter(is_active=True)
    for exam in exams:
        exam_perf, _ = ExamPerformance.objects.get_or_create(
            user=request.user, exam=exam
        )
        exam_perf.update_stats()

    # Update subject performances
    subjects = Subject.objects.filter(is_active=True)
    for subject in subjects:
        subject_perf, _ = SubjectPerformance.objects.get_or_create(
            user=request.user, subject=subject
        )
        subject_perf.update_stats()

    # Update topic performances
    topics = Topic.objects.filter(is_active=True)
    for topic in topics:
        topic_perf, _ = TopicPerformance.objects.get_or_create(
            user=request.user, topic=topic
        )
        topic_perf.update_stats()

    # Update daily activity
    today = timezone.now().date()
    daily_activity, _ = DailyActivity.objects.get_or_create(
        user=request.user, date=today
    )
    daily_activity.save()

    return JsonResponse(
        {
            "status": "success",
            "message": "All stats updated successfully",
            "accuracy": round(performance.overall_accuracy, 1) if performance else 0,
            "total_tests": performance.total_tests_taken if performance else 0,
            "average_score": round(performance.average_score, 1) if performance else 0,
        }
    )


@login_required
def get_recommendations(request):
    """Get AI-powered recommendations based on weak areas (real-time)"""
    # Update all topic stats first
    topics = Topic.objects.filter(is_active=True)
    for topic in topics:
        tp, _ = TopicPerformance.objects.get_or_create(user=request.user, topic=topic)
        tp.update_stats()

    # Get weak topics
    weak_topics = TopicPerformance.objects.filter(
        user=request.user, is_weak=True
    ).select_related("topic", "topic__subject")[:5]

    recommendations = []
    for wt in weak_topics:
        recommendations.append(
            {
                "topic": wt.topic.name,
                "subject": wt.topic.subject.name,
                "accuracy": round(wt.accuracy, 1) if wt.accuracy else 0,
                "questions_attempted": wt.total_questions,
                "suggestion": f"Practice more questions on {wt.topic.name}. Your accuracy is only {wt.accuracy:.1f}%.",
                "practice_url": f"/mock-tests/?topic={wt.topic.id}",
            }
        )

    # Get weak subjects
    weak_subjects = (
        SubjectPerformance.objects.filter(user=request.user)
        .exclude(accuracy__gte=60)
        .order_by("accuracy")[:3]
    )

    for ws in weak_subjects:
        if ws.subject.name not in [r["subject"] for r in recommendations]:
            recommendations.append(
                {
                    "topic": f"{ws.subject.name} (Subject)",
                    "subject": ws.subject.name,
                    "accuracy": round(ws.accuracy, 1) if ws.accuracy else 0,
                    "questions_attempted": ws.total_questions,
                    "suggestion": f"Focus on {ws.subject.name}. Your accuracy is {ws.accuracy:.1f}%.",
                    "practice_url": f"/mock-tests/?subject={ws.subject.id}",
                }
            )

    # Add general recommendations if no weak areas
    if not recommendations:
        recommendations.append(
            {
                "topic": "Keep Going!",
                "subject": "General",
                "accuracy": 100,
                "questions_attempted": 0,
                "suggestion": "Great job! Keep practicing to maintain your performance. Try solving more difficult questions.",
                "practice_url": "/mock-tests/",
            }
        )

    return JsonResponse({"recommendations": recommendations})


@login_required
def get_leaderboard(request):
    """Get real-time leaderboard for top performers"""
    exam_slug = request.GET.get("exam")

    if exam_slug:
        exam = get_object_or_404(Exam, slug=exam_slug)
        # Get top performers for specific exam
        top_performers = (
            UserPerformance.objects.filter(
                user__test_attempts__mock_test__exam=exam,
                user__test_attempts__status="completed",
            )
            .distinct()
            .order_by("-overall_accuracy")[:50]
        )

        exam_name = exam.name
    else:
        # Get overall top performers
        top_performers = UserPerformance.objects.filter(
            total_tests_taken__gt=0
        ).order_by("-overall_accuracy")[:50]
        exam_name = "Overall"

    leaderboard_data = []
    for idx, performer in enumerate(top_performers, 1):
        leaderboard_data.append(
            {
                "rank": idx,
                "username": performer.user.username,
                "full_name": performer.user.get_full_name() or performer.user.username,
                "accuracy": (
                    round(performer.overall_accuracy, 1)
                    if performer.overall_accuracy
                    else 0
                ),
                "tests_taken": performer.total_tests_taken,
                "avg_score": (
                    round(performer.average_score, 1) if performer.average_score else 0
                ),
                "is_current_user": performer.user == request.user,
            }
        )

    return JsonResponse(
        {
            "exam": exam_name,
            "leaderboard": leaderboard_data,
            "total_users": len(leaderboard_data),
            "user_rank": next(
                (p["rank"] for p in leaderboard_data if p["is_current_user"]), None
            ),
        }
    )


@login_required
def get_weekly_progress(request):
    """Get weekly progress data"""
    today = timezone.now().date()
    week_start = today - timedelta(days=7)

    # Get daily activity for last 7 days
    activities = DailyActivity.objects.filter(
        user=request.user, date__gte=week_start
    ).order_by("date")

    # Prepare data
    dates = []
    questions_data = []
    time_data = []
    tests_data = []

    for i in range(7):
        date = today - timedelta(days=6 - i)
        dates.append(date.strftime("%a"))

        # Find activity for this date
        activity = activities.filter(date=date).first()
        if activity:
            questions_data.append(activity.questions_attempted)
            time_data.append(activity.time_spent)
            tests_data.append(activity.tests_taken)
        else:
            questions_data.append(0)
            time_data.append(0)
            tests_data.append(0)

    return JsonResponse(
        {
            "dates": dates,
            "questions": questions_data,
            "time": time_data,
            "tests": tests_data,
        }
    )
