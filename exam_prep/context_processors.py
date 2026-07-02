from django.conf import settings


def seo(request):
    site_url = getattr(settings, "SITE_URL", "https://www.govtexamwala.com").rstrip("/")
    og_image = getattr(settings, "DEFAULT_OG_IMAGE", "").strip()
    if og_image.startswith("/"):
        og_image = f"{site_url}{og_image}"

    private_prefixes = (
        "/accounts/",
        "/admin/",
        "/analytics/",
        "/api/",
        "/payments/",
        "/mock-tests/take/",
        "/mock-tests/results/",
        "/mock-tests/submit/",
        "/study/bookmarks/",
        "/study/my-courses/",
    )
    robots = "noindex, nofollow" if request.path.startswith(private_prefixes) else (
        "index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"
    )

    return {
        "seo": {
            "site_name": getattr(settings, "SITE_NAME", "GovtExamWala"),
            "site_url": site_url,
            "canonical_url": f"{site_url}{request.path}",
            "robots": robots,
            "description": getattr(
                settings,
                "SITE_DESCRIPTION",
                "GovtExamWala helps aspirants prepare for SSC, Banking, Railway, UPSC and other government exams with mock tests, notes, videos and current affairs.",
            ),
            "og_image": og_image,
        }
    }
