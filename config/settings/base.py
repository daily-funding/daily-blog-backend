import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

load_dotenv()


def get_env_or_raise(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ImproperlyConfigured(f"{key} 환경변수가 설정되지 않았습니다.")
    return value


BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOGOUT_REDIRECT_URL = "admin:login"

SECRET_KEY = get_env_or_raise("SECRET_KEY")

POST_IMAGE_UPLOAD_ROOT = "images/posts/"
POST_IMAGE_UPLOAD_URL = "/admin/blog/images/upload/"
BLOG_FRONTEND_URL = "https://blog.dailyfunding.cloud/"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "ckeditor",
    "ckeditor_uploader",
    "blog",
    "rest_framework",
    "django_guid",
]

CKEDITOR_UPLOAD_PATH = POST_IMAGE_UPLOAD_ROOT

CKEDITOR_CONFIGS = {
    "admin_post": {
        "height": 400,
        "width": "100%",
        "toolbar": [
            ["Format", "Bold", "Italic", "Underline", "Strike"],
            ["NumberedList", "BulletedList", "Blockquote"],
            ["Link", "Unlink"],
            ["Image", "Table", "HorizontalRule"],
            ["RemoveFormat", "Source"],
        ],
        "filebrowserImageUploadUrl": POST_IMAGE_UPLOAD_URL,
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django_guid.middleware.guid_middleware",
    "config.middlewares.logging_middleware.LoggingMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middlewares.admin_access_middleware.AdminAccessMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "blog.context_processors.blog_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_env_or_raise("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = get_env_or_raise("AWS_S3_REGION_NAME")

AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 6,
    "EXCEPTION_HANDLER": "config.exceptions.custom_exception_handler",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[{levelname}] {asctime} {name}: {message}",
            "style": "{",
        },
        "medium": {
            "format": "[{levelname}] [{correlation_id}] {asctime} {name}: {message}",
            "style": "{",
        },
    },
}

DJANGO_GUID = {
    "GUID_HEADER_NAME": "Correlation-ID",
    "VALIDATE_GUID": False,
    "RETURN_HEADER": True,
    "EXPOSE_HEADER": True,
    "INTEGRATIONS": [],
    "IGNORE_URLS": [],
    "UUID_LENGTH": 8,
}
