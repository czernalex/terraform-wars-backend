import os
import sys
from pathlib import Path

import sentry_sdk
from decouple import AutoConfig
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration

from main.settings.secrets import Secrets


config = AutoConfig(os.environ.get("DJANGO_CONFIG_ENV_DIR"))

secrets = Secrets(
    SECRET_KEY=config("SECRET_KEY"),
    DB_PASSWORD=config("DB_PASSWORD"),
    EMAIL_HOST_PASSWORD=config("EMAIL_HOST_PASSWORD"),
    SENTRY_DSN=config("SENTRY_DSN", default=None),
)

ENVIRONMENT = config("ENVIRONMENT", default="production")
BASE_DIR = Path(__file__).resolve().parent.parent

BASE_PROTOCOL = config("BASE_PROTOCOL", default="https")
BASE_DOMAIN = config("BASE_DOMAIN")
BASE_URL = f"{BASE_PROTOCOL}://{BASE_DOMAIN}"

FRONTEND_BASE_URL = config("FRONTEND_BASE_URL", default="https://app.terraformwars.com")

DEBUG = config("DEBUG", cast=bool, default=False)
DEBUG_SILK = config("DEBUG_SILK", cast=bool, default=False)

SECRET_KEY = secrets.SECRET_KEY


# Application definition


# Apps

INSTALLED_APPS = [
    "main.apps.api_auth",
    "main.apps.core",
    "main.apps.gcp",
    "main.apps.tasks",
    "main.apps.tutorials",
    "main.apps.users",
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "allauth.headless",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "corsheaders",
    "django_json_widget",
]


# Middleware

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "main.urls"


# Templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "main.apps.core.context_processors.current_year",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                )
            ],
            "builtins": [],
        },
    },
]

# ASGI application

ASGI_APPLICATION = "main.asgi.application"


# WSGI application

WSGI_APPLICATION = "main.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": secrets.DB_PASSWORD,
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

ATOMIC_REQUESTS = False
AUTOCOMMIT = True


# Password validation

AUTH_USER_MODEL = "users.User"

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

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]


# Internationalization

LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/Prague"
USE_TZ = True

USE_I18N = True

USE_L10N = True
USE_THOUSAND_SEPARATOR = True

LANGUAGES = [
    ("en", _("language.en")),
    ("cs", _("language.cs")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# Google Cloud

TASK_API_BASE_URL = config("TASK_API_BASE_URL")
GCP_PROJECT_ID = config("GCP_PROJECT_ID")
GCP_REGION = config("GCP_REGION")
GCP_SERVICE_ACCOUNT_EMAIL = config("GCP_SERVICE_ACCOUNT_EMAIL")
GCP_TERRAFORM_EXECUTOR_SERVICE_ACCOUNT_EMAIL = config("GCP_TERRAFORM_EXECUTOR_SERVICE_ACCOUNT_EMAIL")
GCP_TASKS_TUTORIAL_SUBMISSION_QUEUE_ID = config("GCP_TASKS_TUTORIAL_SUBMISSION_QUEUE_ID")
GCP_TERRAFORM_EXECUTOR_JOB_NAME = config("GCP_TERRAFORM_EXECUTOR_JOB_NAME", "terraform-wars-executor-production-job")


# Static files (CSS, JavaScript, Images)

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_LOCATION = "static"
MEDIA_LOCATION = "media"

USE_CLOUD_STORAGE = config("USE_CLOUD_STORAGE", cast=bool, default=True)

if USE_CLOUD_STORAGE:
    GCS_BUCKET_NAME = config("GCP_STORAGE_BUCKET_NAME")
    common_storage_backend = "storages.backends.gcloud.GoogleCloudStorage"
    common_options = {
        "bucket_name": GCS_BUCKET_NAME,
    }

    STORAGES = {
        "default": {
            "BACKEND": common_storage_backend,
            "OPTIONS": {
                **common_options,
                "location": MEDIA_LOCATION,
                "iam_sign_blob": True,
                "file_overwrite": False,
            },
        },
        "staticfiles": {
            "BACKEND": common_storage_backend,
            "OPTIONS": {
                **common_options,
                "location": STATIC_LOCATION,
                "default_acl": "publicRead",
                "file_overwrite": True,
            },
        },
    }

    GCS_BASE_URL = f"https://storage.googleapis.com/{GCS_BUCKET_NAME}"
    STATIC_URL = f"{GCS_BASE_URL}/{STATIC_LOCATION}/"
    MEDIA_URL = f"{GCS_BASE_URL}/{MEDIA_LOCATION}/"
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.filesystem.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    MEDIA_ROOT = BASE_DIR.parent / MEDIA_LOCATION

    STATIC_URL = f"{BASE_URL}/{STATIC_LOCATION}/"
    MEDIA_URL = f"{BASE_URL}/{MEDIA_LOCATION}/"


## ALLAUTH

ACCOUNT_LOGIN_METHODS = ("email",)
ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "password1*",
]

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False
ACCOUNT_DEFAULT_HTTP_PROTOCOL = BASE_PROTOCOL
ACCOUNT_USER_DISPLAY = lambda user: user.email  # noqa
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_PASSWORD_RESET_BY_CODE_ENABLED = False

### ALLAUTH SOCIALACCOUNT

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "email",
            "profile",
            "https://www.googleapis.com/auth/cloud-platform",
        ],
        "AUTH_PARAMS": {
            "access_type": "offline",
        },
        "OAUTH_PKCE_ENABLED": True,
        "EMAIL_AUTHENTICATION": True,
    }
}
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_STORE_TOKENS = True


### ALLAUTH MFA

MFA_PASSKEY_LOGIN_ENABLED = False
MFA_SUPPORTED_TYPES = [
    "recovery_codes",
    "totp",
]

### ALLAUTH HEADLESS

HEADLESS_ONLY = True
HEADLESS_CLIENTS = ("browser",)
HEADLESS_SERVE_SPECIFICATION = True
HEADLESS_SPECIFICATION_TEMPLATE_NAME = "headless/spec/swagger_cdn.html"

HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": FRONTEND_BASE_URL + "/auth/verify-email/{key}",
    "account_reset_password": FRONTEND_BASE_URL + "/auth/password-reset",
    "account_reset_password_from_key": FRONTEND_BASE_URL + "/auth/password-reset/{key}",
    "account_signup": FRONTEND_BASE_URL + "/auth/sign-up",
    "socialaccount_login_error": FRONTEND_BASE_URL + "/auth/provider-callback",
}


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}


# ALLOWED_HOSTS, CSRF and CORS

SESSION_COOKIE_NAME = "__session"
SESSION_COOKIE_DOMAIN = config("SESSION_COOKIE_DOMAIN")
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", cast=bool, default=True)

CSRF_COOKIE_DOMAIN = config("CSRF_COOKIE_DOMAIN")
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", cast=bool, default=True)

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=lambda v: [s.strip() for s in v.replace('"', "").split(",")])

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "cache-control",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "sentry-trace",
)

CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=lambda v: [s.strip() for s in v.replace('"', "").split(",")])

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", cast=lambda v: [s.strip() for s in v.replace('"', "").split(",")])
if "0.0.0.0" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("0.0.0.0")

SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", cast=bool, default=True)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_HSTS_SECONDS = 3600


# CSP

# FIXME: Configure CSP

# SECURE_CSP = {
#     "default-src": [CSP.SELF],
# }


# Email

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@terraformwars.com")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)


# Sentry

SHELL = "shell" in sys.argv or "shell_plus" in sys.argv

sentry_sdk.init(
    dsn=config("SENTRY_DSN", default=""),
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=0,
    environment=ENVIRONMENT,
    send_default_pii=True,
    ignore_errors=["*"] if SHELL else [],
)


# Unfold Admin


def get_admin_environment() -> list[str]:
    match ENVIRONMENT:
        case "production":
            return ["Production", "danger"]
        case "testing":
            return ["Testing", "warning"]
        case "local":
            return ["Local", "primary"]
        case _:
            raise ValueError(f"Invalid environment: {ENVIRONMENT}")


UNFOLD = {
    "SITE_TITLE": "Terraform Wars",
    "SITE_HEADER": "Terraform Wars",
    "SITE_SUBHEADER": "Site administration",
    "SITE_DROPDOWN": [
        {
            "icon": "web",
            "title": _("App"),
            "link": FRONTEND_BASE_URL,
        },
        {
            "icon": "settings",
            "title": _("Admin"),
            "link": reverse_lazy("admin:index"),
        },
        {
            "icon": "api",
            "title": _("API Docs"),
            "link": reverse_lazy("terraform-wars-api:openapi-view"),
        },
        {
            "icon": "api",
            "title": _("Internal API Docs"),
            "link": reverse_lazy("terraform-wars-internal-api:openapi-view"),
        },
        {
            "icon": "key",
            "title": _("Allauth API Docs"),
            "link": reverse_lazy("headless:openapi_html"),
        },
    ],
    "SITE_URL": FRONTEND_BASE_URL,
    "SITE_SYMBOL": "action_key",
    "SHOW_HISTORY": True,
    "SHOW_BACK_BUTTON": True,
    "ENVIRONMENT": get_admin_environment(),
    "BORDER_RADIUS": "4px",
    "COLORS": {
        "base": {
            "50": "249 250 251",
            "100": "243 244 246",
            "200": "229 231 235",
            "300": "209 213 219",
            "400": "156 163 175",
            "500": "107 114 128",
            "600": "75 85 99",
            "700": "55 65 81",
            "800": "31 41 55",
            "900": "17 24 39",
            "950": "3 7 18",
        },
        "primary": {
            "50": "239, 246, 255",
            "100": "219, 234, 254",
            "200": "191, 219, 254",
            "300": "147, 197, 253",
            "400": "96, 165, 250",
            "500": "59, 130, 246",
            "600": "37, 99, 235",
            "700": "29, 78, 216",
            "800": "30, 64, 175",
            "900": "30, 58, 138",
            "950": "23, 37, 84",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",  # text-base-500
            "subtle-dark": "var(--color-base-400)",  # text-base-400
            "default-light": "var(--color-base-600)",  # text-base-600
            "default-dark": "var(--color-base-300)",  # text-base-300
            "important-light": "var(--color-base-900)",  # text-base-900
            "important-dark": "var(--color-base-100)",  # text-base-100
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("API Auth"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Authenticators"),
                        "icon": "encrypted",
                        "link": reverse_lazy("admin:mfa_authenticator_changelist"),
                        "permission": lambda request: request.user.has_perm("allauth_mfa.view_authenticator"),
                    },
                    {
                        "title": _("Social Account Providers"),
                        "icon": "settings_applications",
                        "link": reverse_lazy("admin:socialaccount_socialapp_changelist"),
                        "permission": lambda request: request.user.has_perm("allauth.view_socialapp"),
                    },
                    {
                        "title": _("Social Accounts"),
                        "icon": "connect_without_contact",
                        "link": reverse_lazy("admin:socialaccount_socialaccount_changelist"),
                        "permission": lambda request: request.user.has_perm("allauth.view_socialaccount"),
                    },
                    {
                        "title": _("Social Tokens"),
                        "icon": "token",
                        "link": reverse_lazy("admin:socialaccount_socialtoken_changelist"),
                        "permission": lambda request: request.user.has_perm("allauth.view_socialtoken"),
                    },
                ],
            },
            {
                "title": _("Tutorials"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Providers"),
                        "icon": "cloud",
                        "link": reverse_lazy("admin:tutorials_provider_changelist"),
                        "permission": lambda request: request.user.has_perm("tutorials.view_provider"),
                    },
                    {
                        "title": _("Tutorials"),
                        "icon": "code_blocks",
                        "link": reverse_lazy("admin:tutorials_tutorial_changelist"),
                        "permission": lambda request: request.user.has_perm("tutorials.view_tutorial"),
                    },
                    {
                        "title": _("Tutorial Projects"),
                        "icon": "folder_supervised",
                        "link": reverse_lazy("admin:tutorials_tutorialproject_changelist"),
                        "permission": lambda request: request.user.has_perm("tutorials.view_tutorialproject"),
                    },
                    {
                        "title": _("Submissions"),
                        "icon": "data_object",
                        "link": reverse_lazy("admin:tutorials_tutorialsubmission_changelist"),
                        "permission": lambda request: request.user.has_perm("tutorials.view_tutorialsubmission"),
                    },
                    {
                        "title": _("Tags"),
                        "icon": "shoppingmode",
                        "link": reverse_lazy("admin:tutorials_tutorialtag_changelist"),
                        "permission": lambda request: request.user.has_perm("tutorials.view_tutorialtag"),
                    },
                ],
            },
            {
                "title": _("Users"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:users_user_changelist"),
                        "permission": lambda request: request.user.has_perm("users.view_user"),
                    },
                    {
                        "title": _("Email Addresses"),
                        "icon": "email",
                        "link": reverse_lazy("admin:account_emailaddress_changelist"),
                        "permission": lambda request: request.user.has_perm("accounts.view_emailaddress"),
                    },
                    {
                        "title": _("Auth Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.has_perm("auth.view_group"),
                    },
                ],
            },
        ],
    },
}
