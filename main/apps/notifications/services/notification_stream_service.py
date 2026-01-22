import asyncio
import logging
from datetime import timedelta
from typing import AsyncIterator

from django.utils import timezone
from injector import inject

from main.apps.notifications.schemas import NotificationListFilterSchema
from main.apps.notifications.services.notification_retrieval_service import NotificationRetrievalService
from main.apps.notifications.services.notification_update_service import NotificationUpdateService
from main.apps.notifications.services.notification_event_builder import NotificationEventBuilder
from main.apps.users.models import User


logger = logging.getLogger(__name__)


class NotificationStreamService:
    @inject
    def __init__(
        self,
        notification_retrieval_service: NotificationRetrievalService,
        notification_update_service: NotificationUpdateService,
        notification_event_builder: NotificationEventBuilder,
    ):
        self.notification_retrieval_service = notification_retrieval_service
        self.notification_update_service = notification_update_service
        self.notification_event_builder = notification_event_builder

    async def stream(self, user: User) -> AsyncIterator[str]:
        while True:
            now = timezone.now()
            notifications = self.notification_retrieval_service.get_list(
                NotificationListFilterSchema(
                    user_id=user.id,
                    dispatched=False,
                    created_at=now - timedelta(seconds=10),
                )
            )
            async for notification in notifications:
                yield self.notification_event_builder.build_event(notification)
                await self.notification_update_service.mark_as_dispatched(notification)

            # FIXME: Remove this polling pattern, instead think of event driven approach
            await asyncio.sleep(1)
