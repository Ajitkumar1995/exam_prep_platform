from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import F, Q
from .models import Notification, Announcement, NotificationView, NotificationClick


def get_navbar_notifications(request):
    """AJAX endpoint to get notifications for navbar"""
    notifications = (
        Notification.objects.filter(
            is_active=True, show_bell_icon=True, start_date__lte=timezone.now()
        )
        .filter(Q(end_date__isnull=True) | Q(end_date__gte=timezone.now()))
        .order_by("order", "-created_at")[:10]
    )

    # Get or create session key
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    data = []
    for notif in notifications:
        is_viewed = NotificationView.objects.filter(
            notification=notif, session_key=session_key
        ).exists()

        data.append(
            {
                "id": notif.id,
                "title": notif.title,
                "message": notif.message[:80],
                "priority": notif.priority,
                "priority_class": {
                    "urgent": "text-red-600",
                    "high": "text-orange-600",
                    "medium": "text-yellow-600",
                    "low": "text-blue-600",
                }.get(notif.priority, "text-gray-600"),
                "action_url": f"/notifications/track-click/{notif.id}/",
                "created_at": notif.created_at.strftime("%b %d, %Y"),
                "is_viewed": is_viewed,
            }
        )

    unread_count = (
        Notification.objects.filter(
            is_active=True, show_bell_icon=True, start_date__lte=timezone.now()
        )
        .filter(Q(end_date__isnull=True) | Q(end_date__gte=timezone.now()))
        .exclude(views_log__session_key=session_key)
        .count()
    )

    return JsonResponse({"notifications": data, "unread_count": unread_count})


def notification_list(request):
    """View all notifications page"""
    notifications = (
        Notification.objects.filter(is_active=True, start_date__lte=timezone.now())
        .filter(Q(end_date__isnull=True) | Q(end_date__gte=timezone.now()))
        .order_by("-order", "-created_at")
    )

    # Track views
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    notification_ids = list(notifications.values_list("id", flat=True))
    viewed_ids = set(
        NotificationView.objects.filter(
            notification_id__in=notification_ids, session_key=session_key
        ).values_list("notification_id", flat=True)
    )
    NotificationView.objects.bulk_create(
        [
            NotificationView(
                notification_id=notification_id,
                session_key=session_key,
                ip_address=request.META.get("REMOTE_ADDR"),
            )
            for notification_id in notification_ids
            if notification_id not in viewed_ids
        ],
        ignore_conflicts=True,
    )

    paginator = Paginator(notifications, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "notifications": page_obj,
    }
    return render(request, "notifications/list.html", context)


def notification_detail(request, slug):
    """View single notification detail"""
    notification = get_object_or_404(Notification, slug=slug, is_active=True)

    # Track view
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    NotificationView.objects.get_or_create(
        notification=notification,
        session_key=session_key,
        defaults={"ip_address": request.META.get("REMOTE_ADDR")},
    )

    # Update view count
    Notification.objects.filter(pk=notification.pk).update(views=F("views") + 1)
    notification.views += 1

    context = {
        "notification": notification,
    }
    return render(request, "notifications/detail.html", context)


def track_click(request, notification_id):
    """Track notification click"""
    notification = get_object_or_404(Notification, id=notification_id)

    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    NotificationClick.objects.create(
        notification=notification,
        session_key=session_key,
        ip_address=request.META.get("REMOTE_ADDR"),
    )

    Notification.objects.filter(pk=notification.pk).update(clicks=F("clicks") + 1)

    # Redirect to action URL or notification detail
    if notification.action_url:
        return redirect(notification.action_url)
    return redirect("notifications:detail", slug=notification.slug)
