from typing import TYPE_CHECKING, Self
from uuid import UUID

from django.db import models


if TYPE_CHECKING:
    from main.apps.tutorials.models import (
        Provider,
        Tutorial,
        TutorialStep,
        TutorialStepSubmission,
        TutorialTag,
        TutorialProject,
    )


class ProviderQuerySet(models.QuerySet["Provider"]):
    pass


class TutorialQuerySet(models.QuerySet["Tutorial"]):
    pass


class TutorialStepQuerySet(models.QuerySet["TutorialStep"]):
    def for_tutorial(self, tutorial_slug: str) -> Self:
        return self.filter(tutorial__slug=tutorial_slug)


class TutorialStepSubmissionQuerySet(models.QuerySet["TutorialStepSubmission"]):
    pass


class TutorialTagQuerySet(models.QuerySet["TutorialTag"]):
    pass


class TutorialProjectQuerySet(models.QuerySet["TutorialProject"]):
    def for_user(self, user_id: UUID) -> Self:
        return self.filter(user_id=user_id)

    def for_tutorial(self, tutorial_id: UUID) -> Self:
        return self.filter(tutorial_id=tutorial_id)
