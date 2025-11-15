"""
ASGI config for main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from decouple import AutoConfig
from django.core.asgi import get_asgi_application

config = AutoConfig(os.environ.get("DJANGO_CONFIG_ENV_DIR"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", config("DJANGO_SETTINGS_MODULE", default="main.settings"))

application = get_asgi_application()
