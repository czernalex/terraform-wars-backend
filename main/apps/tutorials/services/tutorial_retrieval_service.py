from uuid import UUID

from anydi import singleton
from django.db import models, transaction
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.models import Tutorial
from main.apps.tutorials.schemas import TutorialListFilterSchema


@singleton
class TutorialRetrievalService:
    def _get_tutorial_queryset(
        self, select_related_fields: list[str] = [], prefetch_related_fields: list[str] = []
    ) -> models.QuerySet[Tutorial]:
        return Tutorial.objects.select_related(*select_related_fields).prefetch_related(*prefetch_related_fields)

    def _get_tutorial_for_read(self, tutorial_slug: str) -> Tutorial:
        return self._get_tutorial_queryset(
            select_related_fields=["author", "provider"], prefetch_related_fields=["tags"]
        ).get(slug=tutorial_slug)

    @transaction.atomic
    def _get_tutorial_for_update(self, tutorial_id: UUID) -> Tutorial:
        return (
            self._get_tutorial_queryset(select_related_fields=["author", "provider"], prefetch_related_fields=["tags"])
            .select_for_update(of=("self",))
            .get(id=tutorial_id)
        )

    def get_tutorial_list(self, filters: TutorialListFilterSchema) -> models.QuerySet[Tutorial]:
        return filters.filter(
            self._get_tutorial_queryset(select_related_fields=["provider"], prefetch_related_fields=["tags"]).all()
        )

    def get_tutorial_detail(self, tutorial_slug: str) -> Tutorial:
        try:
            return self._get_tutorial_for_read(tutorial_slug)
        except Tutorial.DoesNotExist:
            raise NotFoundError(_("Tutorial not found"))
