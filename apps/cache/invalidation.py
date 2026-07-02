import logging

from django.core.cache import cache

logger = logging.getLogger(__name__)


PAGE_CACHE_PATTERN = "*views.decorators.cache.cache_page*"
APP_CACHE_PATTERN = "*govtexamwala:v1:*"


def delete_pattern(pattern):
    delete_pattern_fn = getattr(cache, "delete_pattern", None)
    if not delete_pattern_fn:
        return 0

    try:
        return delete_pattern_fn(pattern)
    except Exception as exc:
        logger.warning("Unable to delete cache pattern %s: %s", pattern, exc)
        return 0


def invalidate_public_content_cache():
    """
    Clear shared anonymous page cache and project-level content keys.

    This intentionally does not call cache.clear() because the same Redis
    backend stores Django sessions.
    """
    deleted_pages = delete_pattern(PAGE_CACHE_PATTERN)
    deleted_app_keys = delete_pattern(APP_CACHE_PATTERN)
    logger.debug(
        "Invalidated cache patterns: pages=%s app_keys=%s",
        deleted_pages,
        deleted_app_keys,
    )
