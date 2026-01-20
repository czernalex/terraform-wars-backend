from uuid import UUID

from django.db import models
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.providers.models import Provider


class ProviderRetrievalService:
    def _get_queryset(self) -> models.QuerySet[Provider]:
        return Provider.objects.all()

    def _get_for_read_by_id(self, provider_id: UUID) -> Provider:
        return self._get_queryset().get(id=provider_id)

    def get_list(self) -> models.QuerySet[Provider]:
        return self._get_queryset()

    def get_detail_by_id(self, provider_id: UUID) -> Provider:
        try:
            return self._get_for_read_by_id(provider_id)
        except Provider.DoesNotExist:
            raise NotFoundError(_("Provider not found"))
