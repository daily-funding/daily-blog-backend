from .base import *
import os

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "api.blog.dailyfunding.cloud"]

DEBUG = False

INSTALLED_APPS += []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "3306"),
    }
}

LOGGING["filters"] = {
    "correlation_id": {
        "()": "django_guid.log_filters.CorrelationId",
    },
}

LOGGING["handlers"] = {
    "console": {
        "class": "logging.StreamHandler",
        "formatter": "medium",
        "filters": ["correlation_id"],
    },
    "file": {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "filename": BASE_DIR / "logs" / "prod.log",
        "when": "midnight",
        "interval": 1,
        "backupCount": 30,
        "formatter": "medium",
        "filters": ["correlation_id"],
    }
}

LOGGING["loggers"] = {
    "django_guid": {
        "level": "WARNING",
        "propagate": False,
    },
    "blog": {
        "handlers": ["console", "file"],
        "level": "INFO",
        "propagate": False,
    },
    "django.server": {
        "handlers": ["console"],
        "level": "WARNING",
        "propagate": False,
    },
}

LOGGING["root"] = {
    "handlers": ["console", "file"],
    "level": "INFO",
}
