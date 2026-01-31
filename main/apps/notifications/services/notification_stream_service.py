import asyncio
import logging
from typing import AsyncIterator
from uuid import UUID

from injector import inject

from main.apps.core.services import HeartbeatEventBuilder
from main.apps.notifications.schemas import NotificationEventSchema
from main.apps.notifications.services.notification_hub_service import NotificationHubService
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
        heartbeat_event_builder: HeartbeatEventBuilder,
        notification_hub_service: NotificationHubService,
    ):
        self._notification_retrieval_service = notification_retrieval_service
        self._notification_update_service = notification_update_service
        self._notification_event_builder = notification_event_builder
        self._heartbeat_event_builder = heartbeat_event_builder
        self._notification_hub_service = notification_hub_service

    async def astream(self, user_id: UUID) -> AsyncIterator[str]:
        queue = self._notification_hub_service.add_subscriber(user_id)
        yield self._heartbeat_event_builder.build_event()  # Send initial heartbeat event
        try:
            while True:
                try:
                    notification_id = await asyncio.wait_for(queue.get(), timeout=30.0)
                    notification = await self._notification_retrieval_service.aget_detail_by_id(notification_id)
                    logger.info(f"Notification: {notification.id} sent to the user: {user_id}")
                    notification_event = NotificationEventSchema(
                        id=notification.id,
                        text=notification.text,
                        level=notification.level,
                    )
                    yield self._notification_event_builder.build_event(notification_event)
                except asyncio.TimeoutError:
                    logger.info(
                        f"No new notifications received within the timeout. Sending heartbeat event to the user: {user_id}"
                    )
                    yield self._heartbeat_event_builder.build_event()
        finally:
            self._notification_hub_service.remove_subscriber(user_id, queue)
