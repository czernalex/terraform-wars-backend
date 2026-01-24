from typing import override
from uuid import UUID

from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel
from main.apps.providers.enums import ProviderUserProjectStatus
from main.apps.providers.managers import ProviderUserProjectQuerySet
from main.apps.providers.models import Provider
from main.apps.users.models import User


class ProviderUserProject(AbstractUUIDModel):
    MAX_CONFIGURATION_ATTEMPTS = 5

    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="provider_user_projects")
    provider_id: UUID
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="provider_user_projects")
    user_id: UUID

    status = models.CharField(
        _("Status"),
        max_length=255,
        choices=ProviderUserProjectStatus.choices,
        default=ProviderUserProjectStatus.PENDING,
    )
    configuration_attempts = models.PositiveSmallIntegerField(_("Configuration attempts"), default=0)
    configuration_error = models.TextField(_("Configuration error"), blank=True, default="")

    project_id = models.CharField(_("Project ID"), max_length=255, blank=True, default="")
    name = models.CharField(_("Name"), max_length=255, blank=True, default="")
    description = models.TextField(_("Description"), blank=True, default="")

    config_data = models.JSONField(_("Config data"), default=dict)

    objects = ProviderUserProjectQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["provider_id", "user_id", "project_id"], name="unique_provider_user_project_project_id"
            ),
        ]
        indexes = [GinIndex(fields=["config_data"])]
        verbose_name = _("Provider User Project")
        verbose_name_plural = _("Provider User Projects")
        ordering = ("-created_at",)

    @override
    def __str__(self) -> str:
        return f"[{self.provider}] - {self.user.email}"
