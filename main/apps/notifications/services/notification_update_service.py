import logging
from uuid import UUID

from django.db import transaction
from injector import inject


from main.apps.notifications.models import Notification
from main.apps.notifications.schemas import NotificationPartialUpdateSchema
from main.apps.notifications.services.notification_retrieval_service import NotificationRetrievalService


logger = logging.getLogger(__name__)


class NotificationUpdateService:
    @inject
    def __init__(self, notification_retrieval_service: NotificationRetrievalService):
        self._notification_retrieval_service = notification_retrieval_service

    def _partial_update_notification_with_data(
        self, notification: Notification, data: NotificationPartialUpdateSchema
    ) -> Notification:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(notification, field, value)
        notification.save()
        return notification

    @transaction.atomic
    def partial_update(
        self, user_id: UUID, notification_id: int, data: NotificationPartialUpdateSchema
    ) -> Notification:
        logger.info(f"Updating notification: {notification_id}, user_id: {user_id}, data: {data}")
        notification = self._notification_retrieval_service.get_for_update_by_id(user_id, notification_id)
        notification = self._partial_update_notification_with_data(notification, data)
        logger.info(f"Notification: {notification.id} updated successfully")
        return notification
