import io
import os
from urllib.parse import urlparse
from google.cloud import secretmanager, logging_v2
import google.auth

from .base import *


# GOOGLE CLOUD SETTINGS

# Load the settings from the secret manager
credentials, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
client = secretmanager.SecretManagerServiceClient()
settings_name = "application_settings"
name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

env.read_env(io.StringIO(payload))

logging_client = logging_v2.Client()
handler = logging_client.setup_logging()

CLOUDRUN_SERVICE_URL = os.environ.get("CLOUDRUN_SERVICE_URL")

GS_BUCKET_NAME = env("GS_BUCKET_NAME")
GS_DEFAULT_ACL = "publicRead"

# Django settings

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)

# SSL settings
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Security settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# SECURITY WARNING: define the correct hosts in production!
# CSRF Settings
ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
SESSION_COOKIE_DOMAIN = urlparse(CLOUDRUN_SERVICE_URL).netloc
CSRF_USE_SESSIONS = False

# In dev, we use Cloud SQL
DATABASES = {"default": env.db()}

# Define static storage via django-storages[google]
STATICFILES_DIRS = []
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "gcp": {
            "class": "google.cloud.logging_v2.handlers.CloudLoggingHandler",
            "client": logging_client,
        },
    },
    "loggers": {
        "": {
            "handlers": ["gcp"],
            "level": "INFO",
        },
        "root": {
            "handlers": ["gcp"],
            "level": "INFO",
        },
        "django": {
            "handlers": ["gcp"],
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["gcp"],
            "level": "INFO",
        },
    },
}
