from typing import TYPE_CHECKING, Self
from uuid import UUID

from django.db import models

from main.apps.tutorials.enums import TutorialSubmissionStatus, TutorialVoteValue


if TYPE_CHECKING:
    from main.apps.tutorials.models import (
        Tutorial,
        TutorialSubmission,
        TutorialSubmissionEvent,
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

    def annotate_is_completed(self, user_id: UUID) -> Self:
        return self.annotate(
            _is_completed=models.Exists(
                TutorialSubmission.objects.filter(
                    tutorial_id=models.OuterRef("id"),
                    user_id=user_id,
                    status=TutorialSubmissionStatus.SUCCEEDED,
                )
            )
        )


class TutorialSubmissionQuerySet(models.QuerySet["TutorialSubmission"]):
    def for_user(self, user_id: UUID) -> Self:
        return self.filter(user_id=user_id)


class TutorialSubmissionEventQuerySet(models.QuerySet["TutorialSubmissionEvent"]):
    def for_user(self, user_id: UUID) -> Self:
        return self.filter(tutorial_submission__user_id=user_id)

    def for_tutorial_submission(self, tutorial_submission_id: UUID) -> Self:
        return self.filter(tutorial_submission_id=tutorial_submission_id)


class TutorialTagQuerySet(models.QuerySet["TutorialTag"]):
    pass


class TutorialReviewQuerySet(models.QuerySet["TutorialReview"]):
    pass


class TutorialVoteQuerySet(models.QuerySet["TutorialVote"]):
    pass
