from uuid import UUID
from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel
from main.apps.tutorials.enums import TutorialProjectStatus
from main.apps.tutorials.managers import TutorialProjectQuerySet
from main.apps.tutorials.models import Tutorial
from main.apps.users.models import User


class TutorialProject(AbstractUUIDModel):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="projects")
    tutorial_id: UUID
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    user_id: UUID

    status = models.CharField(
        _("Status"), max_length=255, choices=TutorialProjectStatus.choices, default=TutorialProjectStatus.CREATED
    )
    config_data = models.JSONField(_("Config data"), default=dict)

    objects = TutorialProjectQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tutorial", "user"], name="unique_tutorial_user_project"),
        ]
        indexes = [GinIndex(fields=["config_data"])]
        verbose_name = _("Tutorial Project")
        verbose_name_plural = _("Tutorial Projects")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"[{self.tutorial}] - {self.user.email}"
