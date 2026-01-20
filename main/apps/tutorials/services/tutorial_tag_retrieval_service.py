from django.db import models

from main.apps.tutorials.models import TutorialTag


class TutorialTagRetrievalService:
    def _get_queryset(self) -> models.QuerySet[TutorialTag]:
        return TutorialTag.objects.all()

    def get_list(self) -> models.QuerySet[TutorialTag]:
        return self._get_queryset()
