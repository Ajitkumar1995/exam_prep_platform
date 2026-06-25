from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from apps.mocktests.models import TestAttempt
from .models import (
    UserPerformance,
    ExamPerformance,
    SubjectPerformance,
    TopicPerformance,
    DailyActivity,
)


@receiver(post_save, sender=TestAttempt)
def update_analytics_on_test_completion(sender, instance, created, **kwargs):
    """Update all analytics when a test is completed"""

    # Skip for guest users (user is None)
    if instance.user is None:
        print(f"Skipping analytics for guest user (session: {instance.session_id})")
        return

    # Only update when test is completed
    if instance.status == "completed":
        # Update user performance
        performance, _ = UserPerformance.objects.get_or_create(user=instance.user)
        performance.update_stats()

        # Update exam performance
        exam = instance.mock_test.exam
        exam_perf, _ = ExamPerformance.objects.get_or_create(
            user=instance.user, exam=exam
        )
        exam_perf.update_stats()

        # Update subject and topic performances
        answers = instance.answers.all()
        for answer in answers:
            if answer.question.subject:
                subject_perf, _ = SubjectPerformance.objects.get_or_create(
                    user=instance.user, subject=answer.question.subject
                )
                subject_perf.update_stats()

            if answer.question.topic:
                topic_perf, _ = TopicPerformance.objects.get_or_create(
                    user=instance.user, topic=answer.question.topic
                )
                topic_perf.update_stats()

        # Update daily activity
        today = timezone.now().date()
        daily, _ = DailyActivity.objects.get_or_create(user=instance.user, date=today)
        daily.tests_taken += 1
        daily.questions_attempted += instance.answers.count()
        daily.correct_answers += instance.correct_answers
        daily.wrong_answers += instance.wrong_answers
        daily.time_spent += instance.total_time_taken or 0

        # Update streak
        daily.streak = (
            performance.current_streak if hasattr(performance, "current_streak") else 0
        )
        daily.save()

        print(
            f"✅ Analytics updated for {instance.user.email} - Test: {instance.mock_test.name}"
        )


# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from apps.mocktests.models import TestAttempt
# from .models import UserPerformance, ExamPerformance, SubjectPerformance, TopicPerformance, DailyActivity
# from django.utils import timezone
# from datetime import date

# @receiver(post_save, sender=TestAttempt)
# def update_analytics_on_test_completion(sender, instance, created, **kwargs):
#     """Update all analytics when a test is completed"""

#     # SKIP for guest users (user is None)
#     if instance.user is None:
#         print(f"Skipping analytics for guest user (session: {instance.session_id})")
#         return

#     if instance.status == 'completed':
#         # Update user performance
#         performance, _ = UserPerformance.objects.get_or_create(user=instance.user)
#         performance.update_stats()

#         # Update exam performance
#         exam_perf, _ = ExamPerformance.objects.get_or_create(
#             user=instance.user,
#             exam=instance.mock_test.exam
#         )
#         exam_perf.update_stats()

#         # Update subject and topic performances
#         answers = instance.answers.all()
#         for answer in answers:
#             if answer.question.subject:
#                 subject_perf, _ = SubjectPerformance.objects.get_or_create(
#                     user=instance.user,
#                     subject=answer.question.subject
#                 )
#                 subject_perf.update_stats()

#             if answer.question.topic:
#                 topic_perf, _ = TopicPerformance.objects.get_or_create(
#                     user=instance.user,
#                     topic=answer.question.topic
#                 )
#                 topic_perf.update_stats()

#         # Update daily activity
#         today = timezone.now().date()
#         daily, _ = DailyActivity.objects.get_or_create(user=instance.user, date=today)
#         daily.tests_taken += 1
#         daily.questions_attempted += instance.answers.count()
#         daily.correct_answers += instance.correct_answers
#         daily.wrong_answers += instance.wrong_answers
#         daily.time_spent += instance.total_time_taken or 0
#         daily.save()
