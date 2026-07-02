import logging

from celery import shared_task
from django.utils import timezone

from apps.mocktests.models import TestAttempt
from .models import (
    DailyActivity,
    ExamPerformance,
    SubjectPerformance,
    TopicPerformance,
    UserPerformance,
)

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def update_analytics_for_attempt(self, attempt_id):
    """Recalculate analytics after a completed test attempt."""
    attempt = (
        TestAttempt.objects.select_related("user", "mock_test", "mock_test__exam")
        .prefetch_related("answers__question__subject", "answers__question__topic")
        .filter(id=attempt_id, status="completed", user__isnull=False)
        .first()
    )
    if not attempt:
        logger.debug("Skipping analytics task for unavailable attempt=%s", attempt_id)
        return {"updated": False, "attempt_id": attempt_id}

    performance, _ = UserPerformance.objects.get_or_create(user=attempt.user)
    performance.update_stats()

    exam_perf, _ = ExamPerformance.objects.get_or_create(
        user=attempt.user, exam=attempt.mock_test.exam
    )
    exam_perf.update_stats()

    answers = list(attempt.answers.all())
    subject_ids = {
        answer.question.subject_id for answer in answers if answer.question.subject_id
    }
    topic_ids = {
        answer.question.topic_id for answer in answers if answer.question.topic_id
    }

    for subject_id in subject_ids:
        subject_perf, _ = SubjectPerformance.objects.get_or_create(
            user=attempt.user, subject_id=subject_id
        )
        subject_perf.update_stats()

    for topic_id in topic_ids:
        topic_perf, _ = TopicPerformance.objects.get_or_create(
            user=attempt.user, topic_id=topic_id
        )
        topic_perf.update_stats()

    daily, _ = DailyActivity.objects.get_or_create(
        user=attempt.user, date=timezone.now().date()
    )
    daily.tests_taken += 1
    daily.questions_attempted += attempt.answers.count()
    daily.correct_answers += attempt.correct_answers
    daily.wrong_answers += attempt.wrong_answers
    daily.time_spent += attempt.total_time_taken or 0
    daily.streak = performance.current_streak
    daily.save()

    logger.info(
        "Analytics task updated user=%s attempt=%s",
        attempt.user.email,
        attempt.id,
    )
    return {"updated": True, "attempt_id": attempt.id, "user_id": attempt.user_id}
