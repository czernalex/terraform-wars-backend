import logging
from typing import Iterable, Sequence
from uuid import UUID

from django.db import models, transaction
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.models.tutorial_submission import TutorialSubmission
from main.apps.tutorials.schemas import TutorialSubmissionListFilterSchema


logger = logging.getLogger(__name__)


class TutorialSubmissionRetrievalService:
    def _get_queryset(
        self, select_related_fields: Sequence[str] = [], prefetch_related_fields: Sequence[str | models.Prefetch] = []
    ) -> models.QuerySet[TutorialSubmission]:
        return TutorialSubmission.objects.select_related(*select_related_fields).prefetch_related(
            *prefetch_related_fields
        )

    async def _aget_for_read_by_id(self, user_id: UUID, tutorial_submission_id: UUID) -> TutorialSubmission:
        return (
            await self._get_queryset(
                select_related_fields=[
                    "tutorial",
                    "tutorial__provider",
                    "provider_user_project",
                    "user",
                ]
            )
            .for_user(user_id)
            .aget(id=tutorial_submission_id)
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

    def _get_for_update_by_id(self, user_id: UUID, tutorial_submission_id: UUID) -> TutorialSubmission:
        return (
            self._get_queryset(
                select_related_fields=[
                    "tutorial",
                    "tutorial__provider",
                    "provider_user_project",
                    "user",
                ]
            )
            .select_for_update(of=("self",))
            .for_user(user_id)
            .get(id=tutorial_submission_id)
        )

    def get_list(
        self, filters: TutorialSubmissionListFilterSchema, ordering: Iterable[str] = ("-created_at",)
    ) -> models.QuerySet[TutorialSubmission]:
        return filters.filter(
            self._get_queryset(
                select_related_fields=[
                    "tutorial",
                    "tutorial__provider",
                    "provider_user_project",
                    "provider_user_project__provider",
                    "user",
                ]
            )
        ).order_by(*ordering)

    async def aget_detail_by_id(self, user_id: UUID, tutorial_submission_id: UUID) -> TutorialSubmission:
        try:
            return await self._aget_for_read_by_id(user_id, tutorial_submission_id)
        except TutorialSubmission.DoesNotExist:
            logger.warning(f"Tutorial submission: {tutorial_submission_id} not found for user: {user_id}")
            raise NotFoundError(_("Tutorial submission not found"))

    def get_detail_by_id(self, user_id: UUID, tutorial_submission_id: UUID) -> TutorialSubmission:
        try:
            return self._get_for_read_by_id(user_id, tutorial_submission_id)
        except TutorialSubmission.DoesNotExist:
            logger.warning(f"Tutorial submission: {tutorial_submission_id} not found for user: {user_id}")
            raise NotFoundError(_("Tutorial submission not found"))

    @transaction.atomic
    def get_for_update_by_id(self, user_id: UUID, tutorial_submission_id: UUID) -> TutorialSubmission:
        try:
            return self._get_for_update_by_id(user_id, tutorial_submission_id)
        except TutorialSubmission.DoesNotExist:
            logger.warning(f"Tutorial submission: {tutorial_submission_id} not found for user: {user_id}")
            raise NotFoundError(_("Tutorial submission not found"))
