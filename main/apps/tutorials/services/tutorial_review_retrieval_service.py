from typing import Sequence

from django.db import models

from main.apps.tutorials.models import TutorialReview
from main.apps.tutorials.schemas import TutorialReviewListFilterSchema


class TutorialReviewRetrievalService:
    def _get_queryset(
        self, select_related_fields: Sequence[str] = [], prefetch_related_fields: Sequence[str | models.Prefetch] = []
    ) -> models.QuerySet[TutorialReview]:
        return TutorialReview.objects.select_related(*select_related_fields).prefetch_related(*prefetch_related_fields)

    def get_list(self, filters: TutorialReviewListFilterSchema) -> models.QuerySet[TutorialReview]:
        return filters.filter(self._get_queryset(select_related_fields=["user"]))
