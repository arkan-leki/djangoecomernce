"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import environ
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["http://ecommerce-dev.eu-central-1.elasticbeanstalk.com/"]
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_components",
    "store",
    "cart",
    "accounts",
    "payment",
    "mathfilters",
    "crispy_forms",
    "crispy_bootstrap4",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecommerce.urls"
AUTH_USER_MODEL = "accounts.CustomUser"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "store.views.categories",
                "cart.context_processors.cart",
            ],
            'builtins': [
                'django_components.templatetags.component_tags',
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        # Default Django loader
                        "django.template.loaders.filesystem.Loader",
                        # Inluding this is the same as APP_DIRS=True
                        "django.template.loaders.app_directories.Loader",
                        # Components loader
                        "django_components.template_loader.Loader",
                    ],
                )
            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = "bootstrap4"

WSGI_APPLICATION = "ecommerce.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': env('DATABASE_NAME'),
    #     'USER': env('DATABASE_USER'),
    #     'PASSWORD': env('DATABASE_PASS'),
    #     'HOST': 'djangoecomernce.cxaw1emz4xnd.eu-central-1.rds.amazonaws.com',
    #     'PORT': '5432',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Use SMTP email backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# SMTP email settings
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "arkan.leki@gmail.com"
EMAIL_HOST_PASSWORD = "yuacvabggtidtgnz"


# paypal popup
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

USE_S3 = False

if USE_S3:
    # Media AND STATIC FILE
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    # aws settings
    AWS_ACCESS_KEY_ID = env("AWS_SECRET_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_KEY")
    S3_BUCKET_NAME = "arkanecommernce"
    AWS_STORAGE_BUCKET_NAME = "arkanecommernce"
    AWS_DEFAULT_ACL = None
    AWS_S3_FILE_OVERWEITE = False
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    STATIC_LOCATION = "static"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
else:
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.2/howto/static-files/
    STATIC_URL = "static/"
    STATICFILES_DIRS = [BASE_DIR / "components", BASE_DIR / "static"]
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "static/media"
    STATIC_ROOT = BASE_DIR / "static_root"
