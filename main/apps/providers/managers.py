from typing import TYPE_CHECKING, Self

from django.db import models
from django.db.models.expressions import UUID


if TYPE_CHECKING:
    from main.apps.providers.models import Provider, ProviderUserProject


class ProviderQuerySet(models.QuerySet["Provider"]):
    pass


class ProviderUserProjectQuerySet(models.QuerySet["ProviderUserProject"]):
    def for_user(self, user_id: UUID) -> Self:
        return self.filter(user_id=user_id)
