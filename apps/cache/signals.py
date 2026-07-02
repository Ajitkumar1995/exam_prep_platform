from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.cache.invalidation import invalidate_public_content_cache
from apps.exams.models import (
    DailyChallenge,
    Exam,
    ExamAnnouncement,
    ExamCategory,
    ExamFaq,
    LiveTestCard,
    Question,
    StudyMaterial,
    Subject,
    Topic,
)
from apps.interviews.models import InterviewCategory, InterviewQuestion
from apps.mocktests.models import MockTest, MockTestQuestion
from apps.notifications.models import Announcement, Notification
from apps.study_materials.models import (
    Course,
    CourseCategory,
    CurrentAffair,
    EBook,
    Lecture,
    Note,
    Section,
    VideoLecture,
)


CONTENT_MODELS = (
    Announcement,
    Course,
    CourseCategory,
    CurrentAffair,
    DailyChallenge,
    EBook,
    Exam,
    ExamAnnouncement,
    ExamCategory,
    ExamFaq,
    InterviewCategory,
    InterviewQuestion,
    Lecture,
    LiveTestCard,
    MockTest,
    MockTestQuestion,
    Note,
    Notification,
    Question,
    Section,
    StudyMaterial,
    Subject,
    Topic,
    VideoLecture,
)


@receiver(post_save, sender=None)
def invalidate_on_save(sender, **kwargs):
    if sender in CONTENT_MODELS:
        invalidate_public_content_cache()


@receiver(post_delete, sender=None)
def invalidate_on_delete(sender, **kwargs):
    if sender in CONTENT_MODELS:
        invalidate_public_content_cache()
