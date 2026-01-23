import asyncio
import logging
from datetime import timedelta
from typing import AsyncIterator, Optional
from uuid import UUID

from django.utils import timezone
from injector import inject

from main.apps.notifications.schemas import NotificationListFilterSchema
from main.apps.notifications.services.notification_retrieval_service import NotificationRetrievalService
from main.apps.notifications.services.notification_update_service import NotificationUpdateService
from main.apps.notifications.services.notification_event_builder import NotificationEventBuilder


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

    def try_cast_last_event_id(self, last_event_id: Optional[str]) -> Optional[int]:
        if last_event_id:
            try:
                return int(last_event_id)
            except ValueError:
                logger.warning(f"Invalid last event ID: {last_event_id}")
                return

    async def stream(self, user_id: UUID, last_event_id: Optional[str] = None) -> AsyncIterator[str]:
        last_event_id = self.try_cast_last_event_id(last_event_id)
        while True:
            now = timezone.now()
            notifications = self.notification_retrieval_service.get_list(
                NotificationListFilterSchema(
                    user_id=user_id,
                    dispatched=False,
                    last_event_id=last_event_id,
                    created_at=now - timedelta(seconds=10) if last_event_id is None else None,
                )
            )
            async for notification in notifications:
                yield self.notification_event_builder.build_event(notification)
                await self.notification_update_service.mark_as_dispatched(notification)

            # FIXME: Remove this polling pattern, instead think of event driven approach
            await asyncio.sleep(5)
