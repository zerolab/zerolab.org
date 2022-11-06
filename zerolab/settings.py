from pathlib import Path

import environ
from whitenoise.compress import Compressor as WhitenoiseCompressor

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    BASE_HOSTNAME=(str, "zerolab.org"),
    SENTRY_DSN=(str, ""),
)

# load local secrets
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"] if DEBUG else env.list("ALLOWED_HOSTS", default=[])


# Application definition
INSTALLED_APPS = [
    "zerolab.core",
    "zerolab.home",
    "zerolab.media",
    "zerolab.search",
    "wagtail.contrib.settings",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "corsheaders",
    "sri",
    "wagtail_2fa",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "wagtail_2fa.middleware.VerifyUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "csp.middleware.CSPMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
]

ROOT_URLCONF = "zerolab.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
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

WSGI_APPLICATION = "zerolab.wsgi.application"


DATABASES = {"default": env.db(default=f"sqlite:///{BASE_DIR}/db.sqlite3")}

CACHES = {
    "default": env.cache(default="dummycache://"),
    "renditions": env.cache(
        var="RENDITION_CACHE_URL", default="locmemcache://renditions"
    ),
}

WAGTAIL_REDIRECTS_FILE_STORAGE = "cache"

# Internationalization
LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [BASE_DIR / "static"]

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = "static/collected"
STATIC_URL = "static/"

WHITENOISE_ALLOW_ALL_ORIGINS = False

WHITENOISE_SKIP_COMPRESS_EXTENSIONS = list(
    WhitenoiseCompressor.SKIP_COMPRESS_EXTENSIONS
) + ["map"]

WHITENOISE_AUTOREFRESH = DEBUG

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

WAGTAILDOCS_DOCUMENT_MODEL = "media.CustomDocument"
WAGTAILIMAGES_IMAGE_MODEL = "media.CustomImage"

WAGTAILIMAGES_FORMAT_CONVERSIONS = {
    "webp": "webp",
    "jpeg": "webp",
    "png": "webp",
}

# S3 configuration
if "AWS_STORAGE_BUCKET_NAME" in env:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False

    if "AWS_S3_CUSTOM_DOMAIN" in env:
        AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")

    INSTALLED_APPS += ("storages",)


# Wagtail
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

WAGTAIL_SITE_NAME = "zerolab.org"

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
        "AUTO_UPDATE": True,
        "ATOMIC_REBUILD": True,
    }
}

WAGTAILADMIN_BASE_URL = f"https://{env('BASE_HOSTNAME')}"

WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAIL_PASSWORD_RESET_ENABLED = False
WAGTAIL_WORKFLOW_ENABLED = False
WAGTAIL_MODERATION_ENABLED = False
WAGTAIL_ENABLE_WHATS_NEW_BANNER = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s][%(process)d][%(levelname)s][%(name)s] %(message)s"
        }
    },
    "loggers": {
        "zerolab": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "wagtail": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# Security
CORS_ALLOWED_ORIGINS = [WAGTAILADMIN_BASE_URL]
WAGTAIL_2FA_REQUIRED = not DEBUG

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"

SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_AGE = 2419200  # About a month
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

PERMISSIONS_POLICY: dict[str, list] = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "document-domain": [],
    "encrypted-media": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "interest-cohort": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
}

# Disable default CSP which blocks all remote content
CSP_DEFAULT_SRC = None

if not DEBUG:
    CSP_BLOCK_ALL_MIXED_CONTENT = True
    CSP_UPGRADE_INSECURE_REQUESTS = True

    SECURE_SSL_REDIRECT = True
    SECURE_REDIRECT_EXEMPT = [r"^-/"]

    SECURE_HSTS_SECONDS = 2592000  # 30 days
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
        "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False
    )

    CORS_ALLOWED_ORIGINS = []
    CORS_ALLOW_ALL_ORIGINS = True
