from .settings import *

# Use SQLite for local testing (no PostgreSQL needed)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Use memory cache instead of Redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Disable Celery for local testing
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Use console email backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Disable rate limiting for testing
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {"anon": "1000/day", "user": "10000/day"}

DEBUG = True
