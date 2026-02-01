import logging

from django.db import transaction

from main.apps.tutorials.models import TutorialVote
from main.apps.tutorials.enums import TutorialVoteValue


logger = logging.getLogger(__name__)


class TutorialVoteUpdateService:
    @transaction.atomic
    def update(self, tutorial_vote: TutorialVote, vote_value: TutorialVoteValue) -> TutorialVote:
        logger.info(f"Updating tutorial vote: {tutorial_vote.id} with vote value: {vote_value}")
        tutorial_vote.vote_value = vote_value
        tutorial_vote.save()
        logger.info(f"Tutorial vote updated: {tutorial_vote.id}")
        return tutorial_vote
