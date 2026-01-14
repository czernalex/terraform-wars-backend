from typing import Optional
from uuid import UUID

from django.db import models, transaction
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.schemas import TutorialProjectListFilterSchema
from main.apps.users.models import User
from main.apps.tutorials.models import TutorialProject


class TutorialProjectRetrievalService:
    def _get_tutorial_project_queryset(
        self,
        user_id: UUID,
        select_related_fields: list[str] = [],
        prefetch_related_fields: list[str | models.Prefetch] = [],
    ) -> models.QuerySet[TutorialProject]:
        return (
            TutorialProject.objects.select_related(*select_related_fields)
            .prefetch_related(*prefetch_related_fields)
            .for_user(user_id)
        )

    def _get_tutorial_project_for_read_by_id(self, user_id: UUID, tutorial_project_id: UUID) -> TutorialProject:
        return self._get_tutorial_project_queryset(
            user_id,
            select_related_fields=[
                "tutorial",
                "tutorial__provider",
                "user",
            ],
            prefetch_related_fields=[
                "tutorial__tags",
            ],
        ).get(id=tutorial_project_id)

    def _get_tutorial_project_for_update_by_id(self, user_id: UUID, tutorial_project_id: UUID) -> TutorialProject:
        return (
            self._get_tutorial_project_queryset(
                user_id,
                select_related_fields=[
                    "tutorial",
                    "tutorial__provider",
                    "user",
                ],
                prefetch_related_fields=[
                    "tutorial__tags",
                ],
            )
            .select_for_update(of=("self",))
            .get(id=tutorial_project_id)
        )

    def get_tutorial_project_list(
        self, user: User, filters: TutorialProjectListFilterSchema
    ) -> models.QuerySet[TutorialProject]:
        return filters.filter(
            self._get_tutorial_project_queryset(
                user.id,
                select_related_fields=["tutorial", "tutorial__provider", "user"],
                prefetch_related_fields=["tutorial__tags"],
            ).all()
        )

    def get_tutorial_project_detail_by_id(self, user: User, tutorial_project_id: UUID) -> TutorialProject:
        try:
            return self._get_tutorial_project_for_read_by_id(user.id, tutorial_project_id)
        except TutorialProject.DoesNotExist:
            raise NotFoundError(_("Tutorial project not found"))

    @transaction.atomic
    def get_tutorial_project_for_update_by_id(self, user: User, tutorial_project_id: UUID) -> TutorialProject:
        try:
            return self._get_tutorial_project_for_update_by_id(user.id, tutorial_project_id)
        except TutorialProject.DoesNotExist:
            raise NotFoundError(_("Tutorial project not found"))

    def try_find_tutorial_project_by_tutorial_and_user_id(
        self, tutorial_id: UUID, user_id: UUID
    ) -> Optional[TutorialProject]:
        return (
            self._get_tutorial_project_queryset(
                user_id,
                select_related_fields=[
                    "tutorial",
                    "tutorial__provider",
                    "user",
                ],
                prefetch_related_fields=[
                    "tutorial__tags",
                ],
            )
            .for_tutorial(tutorial_id)
            .first()
        )
