from datetime import date, datetime
from xml.sax.saxutils import escape

from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone


def _site_url():
    return getattr(settings, "SITE_URL", "https://www.govtexamwala.com").rstrip("/")


def _absolute(path):
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{_site_url()}{path}"


def _format_lastmod(value):
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return timezone.now().date().isoformat()


def _url_node(location, lastmod=None, changefreq="weekly", priority="0.7"):
    parts = [
        "  <url>",
        f"    <loc>{escape(location)}</loc>",
        f"    <lastmod>{_format_lastmod(lastmod)}</lastmod>",
        f"    <changefreq>{changefreq}</changefreq>",
        f"    <priority>{priority}</priority>",
        "  </url>",
    ]
    return "\n".join(parts)


def robots_txt(request):
    sitemap_url = _absolute(reverse("sitemap_xml"))
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Disallow: /payments/",
        "Disallow: /analytics/",
        "Disallow: /api/",
        "",
        "User-agent: GPTBot",
        "Allow: /",
        "",
        "User-agent: ChatGPT-User",
        "Allow: /",
        "",
        "User-agent: PerplexityBot",
        "Allow: /",
        "",
        "User-agent: ClaudeBot",
        "Allow: /",
        "",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def llms_txt(request):
    site_name = getattr(settings, "SITE_NAME", "GovtExamWala")
    description = getattr(
        settings,
        "SITE_DESCRIPTION",
        "GovtExamWala helps aspirants prepare for Indian government exams.",
    )
    lines = [
        f"# {site_name}",
        "",
        description,
        "",
        "## Public content",
        "- Exam preparation guides: /exams/",
        "- Mock tests and practice tests: /mock-tests/",
        "- Study notes, videos, ebooks and current affairs: /study/",
        "- Interview preparation: /interviews/",
        "- Contact: /contact/",
        "",
        "## Discovery",
        f"- Sitemap: {_absolute(reverse('sitemap_xml'))}",
        f"- Robots: {_absolute(reverse('robots_txt'))}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    from apps.exams.models import Exam, ExamCategory
    from apps.interviews.models import InterviewCategory
    from apps.mocktests.models import MockTest
    from apps.notifications.models import Notification
    from apps.study_materials.models import CurrentAffair, Note, VideoLecture

    today = timezone.now().date()
    nodes = []

    static_pages = [
        (reverse("home"), "daily", "1.0"),
        (reverse("about"), "monthly", "0.6"),
        (reverse("faq"), "monthly", "0.6"),
        (reverse("privacy_policy"), "yearly", "0.3"),
        (reverse("exams:list"), "daily", "0.9"),
        (reverse("mocktests:list"), "daily", "0.9"),
        (reverse("interviews:home"), "weekly", "0.7"),
        (reverse("interviews:questions"), "weekly", "0.7"),
        (reverse("interviews:tips"), "monthly", "0.6"),
        (reverse("study_materials:home"), "daily", "0.9"),
        (reverse("study_materials:note_list"), "daily", "0.8"),
        (reverse("study_materials:video_list"), "daily", "0.8"),
        (reverse("study_materials:ebook_list"), "weekly", "0.7"),
        (reverse("study_materials:current_affairs_list"), "daily", "0.9"),
        (reverse("contact:contact_us"), "monthly", "0.5"),
    ]
    for path, changefreq, priority in static_pages:
        nodes.append(_url_node(_absolute(path), today, changefreq, priority))

    for category in ExamCategory.objects.filter(is_active=True).only(
        "slug", "updated_at"
    ).iterator():
        nodes.append(
            _url_node(_absolute(category.get_absolute_url()), category.updated_at, "weekly", "0.8")
        )

    for exam in Exam.objects.filter(is_active=True).only(
        "slug", "updated_at"
    ).iterator():
        nodes.append(_url_node(_absolute(exam.get_absolute_url()), exam.updated_at, "weekly", "0.9"))
        nodes.append(
            _url_node(
                _absolute(reverse("exams:mock_tests", args=[exam.slug])),
                exam.updated_at,
                "weekly",
                "0.8",
            )
        )
        nodes.append(
            _url_node(
                _absolute(reverse("exams:study_material", args=[exam.slug])),
                exam.updated_at,
                "weekly",
                "0.8",
            )
        )
        nodes.append(
            _url_node(
                _absolute(reverse("exams:coaching", args=[exam.slug])),
                exam.updated_at,
                "monthly",
                "0.6",
            )
        )

    mock_tests = MockTest.objects.filter(is_active=True).select_related("exam").only(
        "slug", "created_at", "exam__id"
    )
    for mock_test in mock_tests.iterator():
        nodes.append(
            _url_node(_absolute(mock_test.get_absolute_url()), mock_test.created_at, "weekly", "0.85")
        )

    for note in Note.objects.filter(is_active=True).only(
        "slug", "updated_at"
    ).iterator():
        nodes.append(_url_node(_absolute(note.get_absolute_url()), note.updated_at, "weekly", "0.8"))

    for video in VideoLecture.objects.filter(is_active=True).only(
        "slug", "updated_at"
    ).iterator():
        nodes.append(
            _url_node(
                _absolute(reverse("study_materials:video_detail", args=[video.slug])),
                video.updated_at,
                "weekly",
                "0.75",
            )
        )

    for affair in CurrentAffair.objects.filter(is_active=True).only(
        "slug", "updated_at", "date"
    ).iterator():
        nodes.append(
            _url_node(
                _absolute(reverse("study_materials:current_affair_detail", args=[affair.slug])),
                affair.updated_at or affair.date,
                "daily",
                "0.8",
            )
        )

    for category in InterviewCategory.objects.filter(is_active=True).only(
        "slug", "created_at"
    ).iterator():
        nodes.append(
            _url_node(
                _absolute(reverse("interviews:category_questions", args=[category.slug])),
                category.created_at,
                "weekly",
                "0.7",
            )
        )

    active_notifications = Notification.objects.filter(
        is_active=True, start_date__lte=timezone.now()
    ).only("slug", "updated_at", "created_at")
    for notification in active_notifications.iterator():
        nodes.append(
            _url_node(
                _absolute(reverse("notifications:detail", args=[notification.slug])),
                getattr(notification, "updated_at", None) or notification.created_at,
                "weekly",
                "0.65",
            )
        )

    xml = "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            *nodes,
            "</urlset>",
        ]
    )
    return HttpResponse(xml, content_type="application/xml")
