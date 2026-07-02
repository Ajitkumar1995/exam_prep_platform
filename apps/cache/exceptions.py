"""
Cache related exceptions.
"""


class CacheError(Exception):
    """Base cache exception."""


class CacheMiss(CacheError):
    """Raised when cache lookup fails."""


class CacheConnectionError(CacheError):
    """Raised when Redis is unavailable."""