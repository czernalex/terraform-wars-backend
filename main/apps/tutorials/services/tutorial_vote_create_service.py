import logging
from uuid import UUID

from django.db import transaction
from injector import inject

from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.models import TutorialVote
from main.apps.tutorials.schemas import CreateTutorialVoteSchema
from main.apps.tutorials.services.tutorial_vote_retrieval_service import TutorialVoteRetrievalService
from main.apps.tutorials.services.tutorial_vote_update_service import TutorialVoteUpdateService


logger = logging.getLogger(__name__)


class TutorialVoteCreateService:
    @inject
    def __init__(
        self,
        tutorial_vote_retrieval_service: TutorialVoteRetrievalService,
        tutorial_vote_update_service: TutorialVoteUpdateService,
    ):
        self._tutorial_vote_retrieval_service = tutorial_vote_retrieval_service
        self._tutorial_vote_update_service = tutorial_vote_update_service

    def _create_tutorial_vote(self, user_id: UUID, tutorial_id: UUID, data: CreateTutorialVoteSchema) -> TutorialVote:
        return TutorialVote.objects.create(
            tutorial_id=tutorial_id,
            user_id=user_id,
            vote_value=data.vote_value,
        )

    @transaction.atomic
    def create(self, user_id: UUID, tutorial_id: UUID, data: CreateTutorialVoteSchema) -> TutorialVote:
        logger.info(
            f"Creating tutorial vote for user: {user_id} and tutorial: {tutorial_id} with vote value: {data.vote_value}"
        )
        try:
            tutorial_vote = self._tutorial_vote_retrieval_service.get_for_update_by_tutorial_id_and_user_id(
                tutorial_id, user_id
            )
            logger.info(f"Tutorial vote already exists: {tutorial_vote.id}, updating its value.")
            return self._tutorial_vote_update_service.update(tutorial_vote, data.vote_value)
        except NotFoundError:
            tutorial_vote = self._create_tutorial_vote(user_id, tutorial_id, data)
            logger.info(f"Tutorial vote created: {tutorial_vote.id} with vote value: {data.vote_value}")
            return tutorial_vote
