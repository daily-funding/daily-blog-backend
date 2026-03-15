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


