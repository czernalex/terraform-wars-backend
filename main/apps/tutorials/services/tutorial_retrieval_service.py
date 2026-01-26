from typing import Sequence
from uuid import UUID

from django.db import models, transaction
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.models import Tutorial
from main.apps.tutorials.schemas import TutorialListFilterSchema


class TutorialRetrievalService:
    def _get_queryset(
        self, select_related_fields: Sequence[str] = [], prefetch_related_fields: Sequence[str | models.Prefetch] = []
    ) -> models.QuerySet[Tutorial]:
        return Tutorial.objects.select_related(*select_related_fields).prefetch_related(*prefetch_related_fields)

    def _get_for_read_by_slug(self, tutorial_slug: str) -> Tutorial:
        return self._get_queryset(select_related_fields=["author", "provider"], prefetch_related_fields=["tags"]).get(
            slug=tutorial_slug
        )

    def _get_for_read_by_id(self, tutorial_id: UUID) -> Tutorial:
        return self._get_queryset(select_related_fields=["author", "provider"], prefetch_related_fields=["tags"]).get(
            id=tutorial_id
        )

    @transaction.atomic
    def _get_for_update_by_id(self, tutorial_id: UUID) -> Tutorial:
        return (
            self._get_queryset(select_related_fields=["author", "provider"], prefetch_related_fields=["tags"])
            .select_for_update(of=("self",))
            .get(id=tutorial_id)
        )

    def get_list(self, filters: TutorialListFilterSchema) -> models.QuerySet[Tutorial]:
        return filters.filter(
            self._get_queryset(select_related_fields=["provider"], prefetch_related_fields=["tags"]).all()
        )

    def get_detail_by_slug(self, tutorial_slug: str) -> Tutorial:
        try:
            return self._get_for_read_by_slug(tutorial_slug)
        except Tutorial.DoesNotExist:
            raise NotFoundError(_("Tutorial not found"))

    def get_detail_by_id(self, tutorial_id: UUID) -> Tutorial:
        try:
            return self._get_for_read_by_id(tutorial_id)
        except Tutorial.DoesNotExist:
            raise NotFoundError(_("Tutorial not found"))
