from uuid import UUID

from anydi import singleton
from django.db import models, transaction

from main.apps.tutorials.models import Tutorial


@singleton
class TutorialRetrievalService:
    def _get_tutorial_queryset(
        self, select_related_fields: list[str] = [], prefetch_related_fields: list[str] = []
    ) -> models.QuerySet[Tutorial]:
        return Tutorial.objects.select_related(*select_related_fields).prefetch_related(*prefetch_related_fields)

    def get_tutorial_list(self) -> models.QuerySet[Tutorial]:
        return self._get_tutorial_queryset(select_related_fields=["provider"], prefetch_related_fields=["tags"]).all()

    def get_tutorial_for_read(self, tutorial_id: UUID) -> Tutorial:
        return self._get_tutorial_queryset(
            select_related_fields=["author", "provider"], prefetch_related_fields=["tags"]
        ).get(id=tutorial_id)

    @transaction.atomic
    def get_tutorial_for_update(self, tutorial_id: UUID) -> Tutorial:
        return (
            self._get_tutorial_queryset(select_related_fields=["author", "provider"], prefetch_related_fields=["tags"])
            .select_for_update(of=("self",))
            .get(id=tutorial_id)
        )
