import logging
from typing import Iterable
from uuid import UUID

from django.db import models, transaction
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.notifications.models import Notification
from main.apps.notifications.schemas import NotificationListFilterSchema


logger = logging.getLogger(__name__)


class NotificationRetrievalService:
    def _get_queryset(self) -> models.QuerySet[Notification]:
        return Notification.objects.all()

    async def _aget_for_read_by_id(self, notification_id: int) -> Notification:
        return await self._get_queryset().aget(id=notification_id)

    def _get_for_update_by_id(self, user_id: UUID, notification_id: int) -> Notification:
        return self._get_queryset().select_for_update(of=("self",)).for_user(user_id).get(id=notification_id)

    def get_list(
        self, filters: NotificationListFilterSchema, ordering: Iterable[str] = ("-created_at",)
    ) -> models.QuerySet[Notification]:
        return filters.filter(self._get_queryset()).order_by(*ordering)

    @transaction.atomic
    def get_for_update_by_id(self, user_id: UUID, notification_id: int) -> Notification:
        try:
            return self._get_for_update_by_id(user_id, notification_id)
        except Notification.DoesNotExist:
            logger.warning(f"Notification: {notification_id} not found for user: {user_id}")
            raise NotFoundError(_("Notification not found"))

    async def aget_for_read_by_id(self, notification_id: int) -> Notification:
        try:
            return await self._aget_for_read_by_id(notification_id)
        except Notification.DoesNotExist:
            logger.warning(f"Notification: {notification_id} not found")
            raise NotFoundError(_("Notification not found"))
