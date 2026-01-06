from django.db import models
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.models import TutorialStep
from main.apps.tutorials.schemas import TutorialStepListSchema


class TutorialStepRetrievalService:
    def _get_tutorial_step_queryset(
        self,
        tutorial_slug: str,
        select_related_fields: list[str] = [],
        prefetch_related_fields: list[str | models.Prefetch] = [],
    ) -> models.QuerySet[TutorialStep]:
        return (
            TutorialStep.objects.select_related(*select_related_fields)
            .prefetch_related(*prefetch_related_fields)
            .for_tutorial(tutorial_slug)
        )

    def _get_tutorial_step_for_read(self, tutorial_slug: str, tutorial_step_slug: str) -> TutorialStep:
        return self._get_tutorial_step_queryset(
            tutorial_slug,
            select_related_fields=["tutorial", "tutorial__provider", "tutorial__author"],
            prefetch_related_fields=[models.Prefetch("tutorial__tags")],
        ).get(slug=tutorial_step_slug)

    def get_tutorial_step_list(self, tutorial_slug: str) -> models.QuerySet[TutorialStepListSchema]:
        return self._get_tutorial_step_queryset(tutorial_slug, select_related_fields=["tutorial"]).order_by("order")

    def get_tutorial_step_detail(self, tutorial_slug: str, tutorial_step_slug: str) -> TutorialStep:
        try:
            return self._get_tutorial_step_for_read(tutorial_slug, tutorial_step_slug)
        except TutorialStep.DoesNotExist:
            raise NotFoundError(_("Tutorial step not found"))
