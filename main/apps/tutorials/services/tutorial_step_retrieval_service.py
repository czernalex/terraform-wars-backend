from anydi import singleton
from django.db import models

from main.apps.tutorials.models import TutorialStep
from main.apps.tutorials.schemas import TutorialStepListSchema


@singleton
class TutorialStepRetrievalService:
    def _get_tutorial_step_queryset(
        self, tutorial_slug: str, select_related_fields: list[str] = [], prefetch_related_fields: list[str] = []
    ) -> models.QuerySet[TutorialStep]:
        return (
            TutorialStep.objects.select_related(*select_related_fields)
            .prefetch_related(*prefetch_related_fields)
            .for_tutorial(tutorial_slug)
        )

    def _get_tutorial_step_for_read(self, tutorial_slug: str, tutorial_step_slug: str) -> TutorialStep:
        return self._get_tutorial_step_queryset(tutorial_slug, select_related_fields=["tutorial"]).get(
            slug=tutorial_step_slug
        )

    def get_tutorial_step_list(self, tutorial_slug: str) -> models.QuerySet[TutorialStepListSchema]:
        return self._get_tutorial_step_queryset(tutorial_slug, select_related_fields=["tutorial"]).order_by("order")
