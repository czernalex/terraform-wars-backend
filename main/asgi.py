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

os.environ.setdefault("DJANGO_SETTINGS_MODULE", config("DJANGO_SETTINGS_MODULE", default="main.settings.production"))


django_application = get_asgi_application()


async def application(scope, receive, send):
    print(f"ASGI scope: {scope}")
    print(f"ASGI receive: {receive}")
    print(f"ASGI send: {send}")

    if scope["type"] == "http":
        return await django_application(scope, receive, send)

    # loop = asyncio.get_event_loop()
    # notification_stream_setup_service = injector.get(NotificationStreamSetupService)
    # notification_stream_setup_service.setup(loop)
