from typing import TYPE_CHECKING, Self
from uuid import UUID

from django.db import models


if TYPE_CHECKING:
    from main.apps.tutorials.models import (
        Tutorial,
        TutorialSubmission,
        TutorialTag,
        TutorialReview,
    )


class TutorialQuerySet(models.QuerySet["Tutorial"]):
    def for_user(self, user_id: UUID) -> Self:
        return self.filter(author_id=user_id)


class TutorialSubmissionQuerySet(models.QuerySet["TutorialSubmission"]):
    pass


class TutorialTagQuerySet(models.QuerySet["TutorialTag"]):
    pass


class TutorialReviewQuerySet(models.QuerySet["TutorialReview"]):
    pass
