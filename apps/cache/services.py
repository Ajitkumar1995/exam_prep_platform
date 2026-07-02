"""
Centralized Cache Service for GovtExamWala.

All applications should use this service instead of directly
using django.core.cache.cache.

Advantages:
- Centralized Redis access
- Automatic cache hit/miss logging
- Namespace support
- Safe cache operations
- Easy future extensions (locking, metrics, compression, etc.)
"""

import logging
from typing import Any, Callable, Optional

from django.core.cache import cache

logger = logging.getLogger(__name__)


class CacheService:
    """
    Central cache manager.

    Example:

        categories = CacheService.get_or_set(
            key=CacheKeys.exam_categories(),
            timeout=CacheTimeout.EXAM_LIST,
            callback=lambda: ExamCategory.objects.filter(is_active=True),
        )
    """

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Retrieve value from cache.
        """
        value = cache.get(key)

        if value is None:
            logger.debug("[CACHE MISS] %s", key)
            return default

        logger.debug("[CACHE HIT ] %s", key)
        return value

    @staticmethod
    def set(
        key: str,
        value: Any,
        timeout: Optional[int] = None,
    ) -> Any:
        """
        Store value in cache.
        """
        cache.set(key, value, timeout)

        logger.debug("[CACHE SET ] %s", key)

        return value

    @staticmethod
    def delete(key: str) -> None:
        """
        Delete cache key.
        """
        cache.delete(key)

        logger.debug("[CACHE DELETE] %s", key)

    @staticmethod
    def delete_many(keys):
        """
        Delete multiple cache keys.
        """
        cache.delete_many(keys)

        logger.debug("[CACHE DELETE MANY] %s", keys)

    @staticmethod
    def clear():
        """
        Clear entire cache.

        NOTE:
        Avoid calling this in production except for maintenance.
        """
        cache.clear()

        logger.warning("[CACHE CLEAR] Entire cache cleared.")

    @classmethod
    def get_or_set(
        cls,
        key: str,
        timeout: int,
        callback: Callable[[], Any],
    ) -> Any:
        """
        Retrieve cached value.

        If cache is empty:

            1. Execute callback
            2. Store result
            3. Return result

        Example:

            exams = CacheService.get_or_set(
                CacheKeys.exam_list(),
                CacheTimeout.EXAM_LIST,
                lambda: Exam.objects.filter(is_active=True)
            )
        """

        value = cls.get(key)

        if value is not None:
            return value

        value = callback()

        cls.set(key, value, timeout)

        return value

    @staticmethod
    def has_key(key: str) -> bool:
        """
        Check if cache key exists.
        """
        return cache.get(key) is not None

    @staticmethod
    def touch(key: str, timeout: int) -> bool:
        """
        Refresh expiry of cache key.

        Requires Redis backend.
        """
        try:
            return cache.touch(key, timeout)
        except Exception:
            return False

    @staticmethod
    def increment(key: str, delta: int = 1):
        """
        Increment cached integer.
        """
        return cache.incr(key, delta)

    @staticmethod
    def decrement(key: str, delta: int = 1):
        """
        Decrement cached integer.
        """
        return cache.decr(key, delta)

    @staticmethod
    def get_many(keys):
        """
        Retrieve multiple keys in one Redis call.
        """
        return cache.get_many(keys)

    @staticmethod
    def set_many(data: dict, timeout: int = None):
        """
        Store multiple keys in one Redis call.
        """
        cache.set_many(data, timeout)

    @staticmethod
    def cache_info():
        """
        Useful for debugging.
        """
        return {
            "backend": cache.__class__.__name__,
        }