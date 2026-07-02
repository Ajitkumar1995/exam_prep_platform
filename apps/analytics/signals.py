import logging

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from kombu.exceptions import OperationalError
from apps.mocktests.models import TestAttempt
from .tasks import update_analytics_for_attempt

logger = logging.getLogger(__name__)


def _queue_analytics_update(attempt_id):
    """Queue analytics work, falling back inline if the broker is unavailable."""
    try:
        update_analytics_for_attempt.delay(attempt_id)
        logger.info("Analytics task queued for attempt=%s", attempt_id)
    except OperationalError as exc:
        logger.warning(
            "Celery unavailable for analytics attempt=%s: %s", attempt_id, exc
        )
        update_analytics_for_attempt.apply(args=[attempt_id])


@receiver(post_save, sender=TestAttempt)
def update_analytics_on_test_completion(sender, instance, created, **kwargs):
    """Queue analytics recalculation when a registered user completes a test."""

    if instance.user is None:
        logger.debug("Skipping analytics for guest user session=%s", instance.session_id)
        return

    if instance.status == "completed":
        transaction.on_commit(lambda: _queue_analytics_update(instance.id))
