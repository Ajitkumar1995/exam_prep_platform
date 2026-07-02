import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_email_task(
    self,
    subject,
    message,
    recipient_list,
    from_email=None,
    html_message=None,
):
    """Send an email in the background through Django's configured backend."""
    send_mail(
        subject,
        message,
        from_email or settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
        html_message=html_message,
    )
    logger.info("Queued email delivered to %s", ", ".join(recipient_list))
    return {"recipients": recipient_list, "subject": subject}
