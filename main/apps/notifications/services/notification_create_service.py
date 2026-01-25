import logging
from uuid import UUID

import msgspec
from django.db import transaction
from injector import inject

from main.apps.gcp.services import GCPPubSubPublishService
from main.apps.notifications.models import Notification
from main.apps.notifications.schemas import NotificationCreateSchema
from main.apps.notifications.types import NotificationMessage


logger = logging.getLogger(__name__)


class NotificationCreateService:
    @inject
    def __init__(self, gcp_pubsub_publish_service: GCPPubSubPublishService):
        self._gcp_pubsub_publish_service = gcp_pubsub_publish_service

    def _dispatch_notification(self, notification: Notification):
        message = NotificationMessage(
            user_id=notification.user_id,
            notification_id=notification.id,
        )
        transaction.on_commit(
            lambda: self._gcp_pubsub_publish_service.publish("notifications", msgspec.json.encode(message))
        )

    @transaction.atomic
    def create(self, user_id: UUID, data: NotificationCreateSchema) -> Notification:
        notification = Notification.objects.create(
            user_id=user_id,
            text=data.text,
            level=data.level,
        )
        self._dispatch_notification(notification)
        logger.info(f"Notification created: {notification.id}")
        return notification
