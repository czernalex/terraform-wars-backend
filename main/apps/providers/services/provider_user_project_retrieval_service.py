from typing import Sequence
from uuid import UUID

from django.db import models, transaction
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.providers.models.provider_user_project import ProviderUserProject
from main.apps.providers.schemas import ProviderUserProjectListFilterSchema


class ProviderUserProjectRetrievalService:
    def _get_queryset(
        self,
        select_related_fields: Sequence[str] = [],
        prefetch_related_fields: Sequence[str | models.Prefetch] = [],
    ) -> models.QuerySet[ProviderUserProject]:
        return ProviderUserProject.objects.select_related(*select_related_fields).prefetch_related(
            *prefetch_related_fields
        )

    def _get_for_read_by_id(self, user_id: UUID, provider_user_project_id: UUID) -> ProviderUserProject:
        return (
            self._get_queryset(select_related_fields=["provider", "user"])
            .for_user(user_id)
            .get(id=provider_user_project_id)
        )

    def _get_for_update_by_id(self, user_id: UUID, provider_user_project_id: UUID) -> ProviderUserProject:
        return (
            self._get_queryset(select_related_fields=["provider", "user"])
            .select_for_update(of=("self",))
            .for_user(user_id)
            .get(id=provider_user_project_id)
        )

    def get_list(self, filters: ProviderUserProjectListFilterSchema) -> models.QuerySet[ProviderUserProject]:
        qs = self._get_queryset(select_related_fields=["provider", "user"])
        return filters.filter(qs)

    def get_detail_by_id(self, user_id: UUID, provider_user_project_id: UUID) -> ProviderUserProject:
        try:
            return self._get_for_read_by_id(user_id, provider_user_project_id)
        except ProviderUserProject.DoesNotExist:
            raise NotFoundError(_("Provider user project not found"))

    @transaction.atomic
    def get_for_update_by_id(self, user_id: UUID, provider_user_project_id: UUID) -> ProviderUserProject:
        try:
            return self._get_for_update_by_id(user_id, provider_user_project_id)
        except ProviderUserProject.DoesNotExist:
            raise NotFoundError(_("Provider user project not found"))
