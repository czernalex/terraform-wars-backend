from typing import Optional
from uuid import UUID
from django.db import models
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.models import TutorialStep
from main.apps.tutorials.schemas import TutorialStepListSchema


class TutorialStepRetrievalService:
    def _get_queryset(
        self,
        tutorial_slug: Optional[str] = None,
        select_related_fields: list[str] = [],
        prefetch_related_fields: list[str | models.Prefetch] = [],
    ) -> models.QuerySet[TutorialStep]:
        qs = TutorialStep.objects.select_related(*select_related_fields).prefetch_related(*prefetch_related_fields)
        if tutorial_slug:
            qs = qs.for_tutorial(tutorial_slug)
        return qs

    def _get_for_read_by_slug(self, tutorial_slug: str, tutorial_step_slug: str) -> TutorialStep:
        return self._get_queryset(
            tutorial_slug,
            select_related_fields=["tutorial", "tutorial__provider", "tutorial__author"],
            prefetch_related_fields=[models.Prefetch("tutorial__tags")],
        ).get(slug=tutorial_step_slug)

    def _get_for_read_by_id(self, tutorial_step_id: UUID) -> TutorialStep:
        return self._get_queryset(
            select_related_fields=["tutorial", "tutorial__provider", "tutorial__author"],
            prefetch_related_fields=[models.Prefetch("tutorial__tags")],
        ).get(id=tutorial_step_id)

    def get_list(self, tutorial_slug: str) -> models.QuerySet[TutorialStepListSchema]:
        return self._get_queryset(tutorial_slug, select_related_fields=["tutorial"]).order_by("order")

    def get_detail_by_slug(self, tutorial_slug: str, tutorial_step_slug: str) -> TutorialStep:
        try:
            return self._get_for_read_by_slug(tutorial_slug, tutorial_step_slug)
        except TutorialStep.DoesNotExist:
            raise NotFoundError(_("Tutorial step not found"))

    def get_detail_by_id(self, tutorial_step_id: UUID) -> TutorialStep:
        try:
            return self._get_for_read_by_id(tutorial_step_id)
        except TutorialStep.DoesNotExist:
            raise NotFoundError(_("Tutorial step not found"))
