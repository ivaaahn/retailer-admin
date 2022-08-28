"""
Django settings for retailer_admin project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pprint import pprint
from typing import Literal

from dotenv import dotenv_values
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_RETAILER_ADMIN_DIR = Path(__file__).resolve().parent.parent
BASE_PROD_DIR = BASE_RETAILER_ADMIN_DIR
BASE_LOCAL_DIR = BASE_RETAILER_ADMIN_DIR.parent

DEPLOY_MODE = os.environ.get("DEPLOY_MODE", False)

path_to_config = f"{BASE_LOCAL_DIR}/etc/.env.test"
if DEPLOY_MODE:
    path_to_config = f"{BASE_PROD_DIR}/etc/.env.prod"


config = dotenv_values(path_to_config)
pprint(config)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config["DEBUG"]

ALLOWED_HOSTS = ["0.0.0.0", "localhost"]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",
    "https://retailerx.gq",
    "https://www.retailerx.gq",
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "products",
    "product_categories",
    "shops",
    "shop_addresses",
    "shop_products",
    "staff",
    "users",
    "user_addresses",
    "order",
    "storages",
]

AUTH_USER_MODEL = "users.UserModel"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "retailer_admin.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_RETAILER_ADMIN_DIR / "templates"],
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

WSGI_APPLICATION = "retailer_admin.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config["NAME"],
        "USER": config["USER"],
        "PASSWORD": config["PASSWORD"],
        "HOST": config["HOST"],
        "PORT": config["PORT"],
    },
    "migrations": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config["NAME"],
        "USER": config["USER_MIGRATIONS"],
        "PASSWORD": config["USER_MIGRATIONS_PASSWORD"],
        "HOST": config["HOST"],
        "PORT": config["PORT"],
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = f"{BASE_LOCAL_DIR}/static/"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

(
    AWS_S3_ENDPOINT_URL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME,
) = (
    config["S3_ENDPOINT_URL"],
    config["S3_ACCESS_KEY_ID"],
    config["S3_SECRET_ACCESS_KEY"],
    config["S3_BUCKET_NAME"],
)
AWS_S3_CUSTOM_DOMAIN = f"storage.yandexcloud.net/{AWS_STORAGE_BUCKET_NAME}"
STATIC_URL = f"{AWS_S3_CUSTOM_DOMAIN}/"

REDIS_HOST = config["REDIS_HOST"]
REDIS_PORT = config["REDIS_PORT"]
REDIS_DB = config["REDIS_DB"]


if config.get("LOGGING", False):
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}
        },
        "handlers": {
            "mail_admins": {
                "level": "ERROR",
                "filters": ["require_debug_false"],
                "class": "django.utils.log.AdminEmailHandler",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "django.request": {
                "handlers": ["mail_admins"],
                "level": "ERROR",
                "propagate": True,
            },
            "django.db.backends": {"handlers": ["console"], "level": "DEBUG"},
        },
    }
