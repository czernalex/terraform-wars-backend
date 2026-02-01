import logging
from uuid import UUID

from django.db import transaction
from injector import inject

from main.apps.tutorials.services.tutorial_vote_retrieval_service import TutorialVoteRetrievalService


logger = logging.getLogger(__name__)


class TutorialVoteDeleteService:
    @inject
    def __init__(self, tutorial_vote_retrieval_service: TutorialVoteRetrievalService):
        self._tutorial_vote_retrieval_service = tutorial_vote_retrieval_service

    @transaction.atomic
    def delete(self, user_id: UUID, tutorial_id: UUID) -> None:
        logger.info(f"Deleting tutorial vote for user: {user_id} and tutorial: {tutorial_id}")
        tutorial_vote = self._tutorial_vote_retrieval_service.get_for_update_by_tutorial_id_and_user_id(
            tutorial_id, user_id
        )
        tutorial_vote.delete()
        logger.info(f"Tutorial vote deleted: {tutorial_vote.id}")
