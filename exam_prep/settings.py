import os
from pathlib import Path
from decouple import config
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-j283o!g9_3+6x16b16^vc^n!rsufug9e1_71((*!=6ixhpb7oa",
)

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")

# ALLOWED_HOSTS = [
#     "127.0.0.1",
#     "localhost",
#     "govtexamwala.com",
#     "www.govtexamwala.com",
# ]

# CSRF_TRUSTED_ORIGINS = [
#     "https://govtexamwala.com",
#     "https://www.govtexamwala.com",
# ]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "import_export",
    "ckeditor",
    "django_celery_beat",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "drf_yasg",
    # Local apps
    "apps.accounts",
    "apps.exams",
    "apps.mocktests",
    "apps.analytics",
    "apps.interviews",
    "apps.payments",
    "apps.notifications",
    "apps.study_materials",
    "apps.api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "exam_prep.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "exam_prep.wsgi.application"

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME', default='exam_prep'),
#         'USER': config('DB_USER', default='admin'),
#         'PASSWORD': config('DB_PASSWORD', default='admin123'),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='5432'),
#     }
# }

# Comment out PostgreSQL and use SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    # {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    # {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    # {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
# Disable password validators
AUTH_PASSWORD_VALIDATORS = []


LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

LOGIN_URL = "accounts:login_signup"
LOGIN_REDIRECT_URL = "accounts:dashboard"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{config('REDIS_HOST', default='localhost')}:{config('REDIS_PORT', default='6379')}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

CELERY_BROKER_URL = f"redis://{config('REDIS_HOST', default='localhost')}:{config('REDIS_PORT', default='6379')}/0"
CELERY_RESULT_BACKEND = f"redis://{config('REDIS_HOST', default='localhost')}:{config('REDIS_PORT', default='6379')}/0"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "1000/day"},
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    # "https://govtexamwala.com",
    # "https://www.govtexamwala.com",
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# Email settings (for development - prints to console)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="noreply@govtexamwala.com")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="hahvzatzrscwhngg")
DEFAULT_FROM_EMAIL = "GovtExamWala <noreply@govtexamwala.com>"
EMAIL_REPLY_TO = ["support@govtexamwala.com"]
# # Razorpay
# RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID', default='')
# RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET', default='')

# # Razorpay Configuration
# RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_YourKeyHere')
# RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'YourSecretHere')

# PayTM Configuration
PAYTM_ENABLED = True
PAYTM_DEBUG = True  # True for staging, False for production
PAYTM_MID = "YOUR_MID_HERE"  # Get from PayTM dashboard
PAYTM_MERCHANT_KEY = "YOUR_MERCHANT_KEY_HERE"  # Get from PayTM dashboard
PAYTM_WEBSITE_NAME = "WEBSTAGING"  # For staging
PAYTM_INDUSTRY_TYPE = "Retail"
PAYTM_CHANNEL_ID = "WEB"

# Redis for rate limiting
RATELIMIT_USE_CACHE = "default"

# CKEditor config
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": "100%",
    },
}
