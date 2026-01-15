from uuid import UUID

from django.db import models
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.models.tutorial_step_submission import TutorialStepSubmission


class TutorialStepSubmissionRetrievalService:
    def _get_queryset(
        self, select_related_fields: list[str] = [], prefetch_related_fields: list[str] = []
    ) -> models.QuerySet[TutorialStepSubmission]:
        return TutorialStepSubmission.objects.select_related(*select_related_fields).prefetch_related(
            *prefetch_related_fields
        )

    def _get_for_read_by_id(self, tutorial_step_submission_id: UUID) -> TutorialStepSubmission:
        return self._get_queryset(
            select_related_fields=[
                "tutorial_project",
                "tutorial_project__tutorial",
                "tutorial_project__tutorial__provider",
                "tutorial_step",
                "tutorial_step__tutorial",
                "tutorial_step__tutorial__provider",
                "user",
            ]
        ).get(id=tutorial_step_submission_id)

    def get_detail_by_id(self, tutorial_step_submission_id: UUID) -> TutorialStepSubmission:
        try:
            return self._get_for_read_by_id(tutorial_step_submission_id)
        except TutorialStepSubmission.DoesNotExist:
            raise NotFoundError(_("Tutorial step submission not found"))
