import logging
from uuid import UUID

from django.db import transaction
from injector import inject

from main.apps.tutorials.services.tutorial_submission_retrieval_service import TutorialSubmissionRetrievalService
from main.apps.tutorials.services.tutorial_submission_validation_service import TutorialSubmissionValidationService


logger = logging.getLogger(__name__)


class TutorialSubmissionDeleteService:
    @inject
    def __init__(
        self,
        tutorial_submission_retrieval_service: TutorialSubmissionRetrievalService,
        tutorial_submission_validation_service: TutorialSubmissionValidationService,
    ):
        self._tutorial_submission_retrieval_service = tutorial_submission_retrieval_service
        self._tutorial_submission_validation_service = tutorial_submission_validation_service

    @transaction.atomic
    def delete(self, user_id: UUID, tutorial_submission_id: UUID) -> None:
        logger.info(f"Deleting tutorial submission: {tutorial_submission_id} for user: {user_id}")
        tutorial_submission = self._tutorial_submission_retrieval_service.get_for_update_by_id(
            user_id, tutorial_submission_id
        )
        self._tutorial_submission_validation_service.validate_can_be_deleted(tutorial_submission)
        tutorial_submission.delete()
        logger.info(f"Tutorial submission deleted: {tutorial_submission_id}")
