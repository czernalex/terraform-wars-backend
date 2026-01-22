from typing import override
from uuid import UUID

from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractTimestampedModel
from main.apps.notifications.enums import NotificationLevel
from main.apps.notifications.managers import NotificationQuerySet
from main.apps.users.models import User


class Notification(AbstractTimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    user_id: UUID

    text = models.CharField(_("Notification text"), max_length=255)
    level = models.CharField(
        _("Notification level"), max_length=255, choices=NotificationLevel.choices, default=NotificationLevel.INFO
    )
    dispatched = models.BooleanField(_("Dispatched"), default=False)

    objects = NotificationQuerySet.as_manager()

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ("-created_at",)

    @override
    def __str__(self) -> str:
        return f"[{self.user.email}:{self.level}] {self.text}"
