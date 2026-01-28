from typing import Sequence
from uuid import UUID

from django.db import models
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.models.tutorial_submission import TutorialSubmission


class TutorialSubmissionRetrievalService:
    def _get_queryset(
        self, select_related_fields: Sequence[str] = [], prefetch_related_fields: Sequence[str | models.Prefetch] = []
    ) -> models.QuerySet[TutorialSubmission]:
        return TutorialSubmission.objects.select_related(*select_related_fields).prefetch_related(
            *prefetch_related_fields
        )

    def _get_for_read_by_id(self, user_id: UUID, tutorial_submission_id: UUID) -> TutorialSubmission:
        return (
            self._get_queryset(
                select_related_fields=[
                    "tutorial",
                    "tutorial__provider",
                    "provider_user_project",
                    "user",
                ]
            )
            .for_user(user_id)
            .get(id=tutorial_submission_id)
        )

    def get_detail_by_id(self, user_id: UUID, tutorial_submission_id: UUID) -> TutorialSubmission:
        try:
            return self._get_for_read_by_id(user_id, tutorial_submission_id)
        except TutorialSubmission.DoesNotExist:
            raise NotFoundError(_("Tutorial submission not found"))
