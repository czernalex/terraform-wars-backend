from django.db import models

from main.apps.notifications.models import Notification
from main.apps.notifications.schemas import NotificationListFilterSchema


class NotificationRetrievalService:
    def _get_queryset(self) -> models.QuerySet[Notification]:
        return Notification.objects.all()

    def get_list(self, filters: NotificationListFilterSchema) -> models.QuerySet[Notification]:
        return filters.filter(self._get_queryset())
