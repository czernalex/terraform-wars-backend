"""
ASGI config for main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import asyncio

from decouple import AutoConfig
from django.core.asgi import get_asgi_application

from main.apps.tutorials.services import TutorialSubmissionEventStreamSetupService

config = AutoConfig(os.environ.get("DJANGO_CONFIG_ENV_DIR"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", config("DJANGO_SETTINGS_MODULE", default="main.settings.production"))


django_application = get_asgi_application()


async def application(scope, receive, send):
    from main.di import injector
    from main.apps.notifications.services import NotificationStreamSetupService

    if scope["type"] == "http":
        return await django_application(scope, receive, send)

    # We need to setup PubSub suscription, which runs in a separate thread.
    # From the background thread, we pass tasks to the main thread to be executed.
    loop = asyncio.get_event_loop()
    notification_stream_setup_service = injector.get(NotificationStreamSetupService)
    notification_stream_setup_service.setup(loop)
    tutorial_submission_event_stream_setup_service = injector.get(TutorialSubmissionEventStreamSetupService)
    tutorial_submission_event_stream_setup_service.setup(loop)
