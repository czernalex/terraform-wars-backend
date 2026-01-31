from typing import Iterable, Sequence
from uuid import UUID

from django.db import models
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.models.tutorial_submission_event import TutorialSubmissionEvent
from main.apps.tutorials.schemas import TutorialSubmissionEventListFilterSchema


class TutorialSubmissionEventRetrievalService:
    def _get_queryset(self, select_related_fields: Sequence[str]) -> models.QuerySet[TutorialSubmissionEvent]:
        return TutorialSubmissionEvent.objects.select_related(*select_related_fields)

    async def _aget_for_read_by_id(self, user_id: UUID, tutorial_submission_event_id: UUID) -> TutorialSubmissionEvent:
        return (
            await self._get_queryset(select_related_fields=["tutorial_submission", "tutorial_submission__user"])
            .for_user(user_id)
            .aget(id=tutorial_submission_event_id)
        )

    def get_list(
        self, filters: TutorialSubmissionEventListFilterSchema, ordering: Iterable[str] = ("-created_at",)
    ) -> models.QuerySet[TutorialSubmissionEvent]:
        return filters.filter(
            self._get_queryset(select_related_fields=["tutorial_submission", "tutorial_submission__user"])
        ).order_by(*ordering)

    async def aget_for_read_by_id(self, user_id: UUID, tutorial_submission_event_id: UUID) -> TutorialSubmissionEvent:
        try:
            return await self._aget_for_read_by_id(user_id, tutorial_submission_event_id)
        except TutorialSubmissionEvent.DoesNotExist:
            raise NotFoundError(_("Tutorial submission event not found"))
