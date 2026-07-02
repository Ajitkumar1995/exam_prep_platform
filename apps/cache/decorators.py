from functools import wraps

from django.conf import settings
from django.views.decorators.cache import cache_page


def anonymous_cache_page(timeout, key_prefix="page"):
    """
    Cache a full rendered page only for anonymous GET/HEAD requests.

    Authenticated pages often include user-specific nav, messages, purchases,
    attempts, or bookmarks, so they should bypass shared page caching.
    """

    def decorator(view_func):
        cached_view = cache_page(timeout, key_prefix=key_prefix)(view_func)

        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not getattr(settings, "CACHE_ANONYMOUS_PAGES", True):
                return view_func(request, *args, **kwargs)

            if request.method not in ("GET", "HEAD"):
                return view_func(request, *args, **kwargs)

            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)

            return cached_view(request, *args, **kwargs)

        return wrapped

    return decorator
