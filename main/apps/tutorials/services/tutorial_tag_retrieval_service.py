from django.db import models

from main.apps.tutorials.models import TutorialTag


class TutorialTagRetrievalService:
    def get_tutorial_tag_list(self) -> models.QuerySet[TutorialTag]:
        return TutorialTag.objects.all()
