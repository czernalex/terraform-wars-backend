from typing import Sequence
from uuid import UUID

from django.db import models, transaction
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.models import TutorialVote


class TutorialVoteRetrievalService:
    def _get_queryset(
        self, select_related_fields: Sequence[str] = [], prefetch_related_fields: Sequence[str | models.Prefetch] = []
    ) -> models.QuerySet[TutorialVote]:
        return TutorialVote.objects.select_related(*select_related_fields).prefetch_related(*prefetch_related_fields)

    def _get_for_read_by_tutorial_id_and_user_id(self, tutorial_id: UUID, user_id: UUID) -> TutorialVote:
        return self._get_queryset(select_related_fields=["tutorial", "user"]).get(
            tutorial_id=tutorial_id, user_id=user_id
        )

    def _get_for_update_by_tutorial_id_and_user_id(self, tutorial_id: UUID, user_id: UUID) -> TutorialVote:
        return (
            self._get_queryset(select_related_fields=["tutorial", "user"])
            .select_for_update(of=("self",))
            .get(tutorial_id=tutorial_id, user_id=user_id)
        )

    def get_detail_by_tutorial_id_and_user_id(self, tutorial_id: UUID, user_id: UUID) -> TutorialVote:
        try:
            return self._get_for_read_by_tutorial_id_and_user_id(tutorial_id, user_id)
        except TutorialVote.DoesNotExist:
            raise NotFoundError(_("Tutorial vote not found"))

    @transaction.atomic
    def get_for_update_by_tutorial_id_and_user_id(self, tutorial_id: UUID, user_id: UUID) -> TutorialVote:
        try:
            return self._get_for_update_by_tutorial_id_and_user_id(tutorial_id, user_id)
        except TutorialVote.DoesNotExist:
            raise NotFoundError(_("Tutorial vote not found"))
