from .base import *
import os
from dotenv import load_dotenv

load_dotenv()  # .env 읽음

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DEBUG = True

INSTALLED_APPS += [
    #
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LOGGING["handlers"] = {
    "console": {
        "class": "logging.StreamHandler",
        "formatter": "simple",
    },
}

LOGGING["loggers"] = {
    "django_guid": {
        "level": "WARNING",
        "propagate": False,
    },
    "blog": {
        "handlers": ["console"],
        "level": "DEBUG",
        "propagate": False,
    },
}

LOGGING["root"] = {
    "handlers": ["console"],
    "level": "INFO",
}
