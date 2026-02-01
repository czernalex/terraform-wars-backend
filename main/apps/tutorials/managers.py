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
            upvote_count=models.Count(
                "votes", filter=models.Q(votes__vote_value=TutorialVoteValue.UPVOTE), distinct=True
            ),
            downvote_count=models.Count(
                "votes", filter=models.Q(votes__vote_value=TutorialVoteValue.DOWNVOTE), distinct=True
            ),
        )

    def annotate_completed_count(self) -> Self:
        return self.annotate(
            completed_count=models.Count(
                "submissions",
                filter=models.Q(submissions__status=TutorialSubmissionStatus.SUCCEEDED),
                distinct=True,
            )
        )

    def annotate_submissions_count(self) -> Self:
        return self.annotate(
            submissions_count=models.Count(
                "submissions",
                distinct=True,
            )
        )

    def annotate_starred_count(self) -> Self:
        return self.annotate(
            starred_count=models.Count(
                "starred_by",
                distinct=True,
            )
        )

    def annotate_is_completed_by_user(self, user_id: UUID) -> Self:
        from main.apps.tutorials.models.tutorial_submission import TutorialSubmission

        return self.annotate(
            is_completed_by_user=models.Exists(
                TutorialSubmission.objects.filter(
                    tutorial_id=models.OuterRef("id"),
                    user_id=user_id,
                    status=TutorialSubmissionStatus.SUCCEEDED,
                )
            )
        )

    def annotate_stats(self, user_id: UUID) -> Self:
        return (
            self.annotate_vote_count()
            .annotate_completed_count()
            .annotate_submissions_count()
            .annotate_starred_count()
            .annotate_is_completed_by_user(user_id)
        )


class TutorialSubmissionQuerySet(models.QuerySet["TutorialSubmission"]):
    def for_user(self, user_id: UUID) -> Self:
        return self.filter(user_id=user_id)

    def for_tutorial(self, tutorial_id: UUID) -> Self:
        return self.filter(tutorial_id=tutorial_id)

    def for_status(self, status: TutorialSubmissionStatus) -> Self:
        return self.filter(status=status)


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
    def for_tutorial(self, tutorial_id: UUID) -> Self:
        return self.filter(tutorial_id=tutorial_id)

    def for_vote_value(self, vote_value: TutorialVoteValue) -> Self:
        return self.filter(vote_value=vote_value)
