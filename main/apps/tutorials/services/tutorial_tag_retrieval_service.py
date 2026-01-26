from django.db import models

from main.apps.tutorials.models import TutorialTag
from main.apps.tutorials.schemas import TutorialTagListFilterSchema


class TutorialTagRetrievalService:
    def _get_queryset(self) -> models.QuerySet[TutorialTag]:
        return TutorialTag.objects.all()

    def get_list(self, filters: TutorialTagListFilterSchema) -> models.QuerySet[TutorialTag]:
        return filters.filter(self._get_queryset())
