from typing import TYPE_CHECKING, Self
from uuid import UUID

from django.db import models

from main.apps.tutorials.enums import TutorialVoteValue


if TYPE_CHECKING:
    from main.apps.tutorials.models import (
        Tutorial,
        TutorialSubmission,
        TutorialTag,
        TutorialReview,
        TutorialVote,
    )


class TutorialQuerySet(models.QuerySet["Tutorial"]):
    def for_user(self, user_id: UUID) -> Self:
        return self.filter(author_id=user_id)

    def annotate_vote_count(self) -> Self:
        return self.annotate(
            _upvote_count=models.Count("votes", filter=models.Q(votes__vote_value=TutorialVoteValue.UPVOTE)),
            _downvote_count=models.Count("votes", filter=models.Q(votes__vote_value=TutorialVoteValue.DOWNVOTE)),
        )


class TutorialSubmissionQuerySet(models.QuerySet["TutorialSubmission"]):
    def for_user(self, user_id: UUID) -> Self:
        return self.filter(user_id=user_id)


class TutorialTagQuerySet(models.QuerySet["TutorialTag"]):
    pass


class TutorialReviewQuerySet(models.QuerySet["TutorialReview"]):
    pass


class TutorialVoteQuerySet(models.QuerySet["TutorialVote"]):
    pass
