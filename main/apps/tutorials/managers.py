from typing import TYPE_CHECKING, Self
from uuid import UUID

from django.db import models


if TYPE_CHECKING:
    from main.apps.tutorials.models import (
        Provider,
        Tutorial,
        TutorialSubmission,
        TutorialTag,
        TutorialProject,
    )


class ProviderQuerySet(models.QuerySet["Provider"]):
    pass


class TutorialQuerySet(models.QuerySet["Tutorial"]):
    pass


class TutorialSubmissionQuerySet(models.QuerySet["TutorialSubmission"]):
    pass


class TutorialTagQuerySet(models.QuerySet["TutorialTag"]):
    pass


class TutorialProjectQuerySet(models.QuerySet["TutorialProject"]):
    def for_user(self, user_id: UUID) -> Self:
        return self.filter(user_id=user_id)

    def for_tutorial(self, tutorial_id: UUID) -> Self:
        return self.filter(tutorial_id=tutorial_id)
