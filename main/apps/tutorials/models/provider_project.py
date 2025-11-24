from typing import override

from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel
from main.apps.tutorials.models import Provider
from main.apps.users.models import User


class ProviderProject(AbstractUUIDModel):
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, related_name="projects")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")

    class Meta:
        # TODO: Consider if this constraint is really necessary
        constraints = [
            models.UniqueConstraint(fields=["provider", "user"], name="unique_provider_user"),
        ]
        verbose_name = _("Provider Project")
        verbose_name_plural = _("Provider Projects")
        ordering = ("-created_at",)

    @override
    def __str__(self) -> str:
        return f"[{self.provider.name}] - {self.user.email}"
