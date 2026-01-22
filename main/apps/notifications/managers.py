from typing import Self, TYPE_CHECKING
from uuid import UUID

from django.db import models


if TYPE_CHECKING:
    from main.apps.notifications.models import Notification


class NotificationQuerySet(models.QuerySet["Notification"]):
    def for_user(self, user_id: UUID) -> Self:
        return self.filter(user_id=user_id)
