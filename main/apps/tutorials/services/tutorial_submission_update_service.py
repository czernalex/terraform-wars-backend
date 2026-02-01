import logging

from injector import inject

from main.apps.tutorials.enums import TutorialSubmissionStatus
from main.apps.tutorials.models.tutorial_submission import TutorialSubmission
from main.apps.tutorials.schemas import TutorialSubmissionListFilterSchema
from main.apps.tutorials.services.tutorial_submission_retrieval_service import TutorialSubmissionRetrievalService


logger = logging.getLogger(__name__)


class TutorialSubmissionUpdateService:
    @inject
    def __init__(self, tutorial_submission_retrieval_service: TutorialSubmissionRetrievalService):
        self._tutorial_submission_retrieval_service = tutorial_submission_retrieval_service

    def update_status(
        self, tutorial_submission: TutorialSubmission, status: TutorialSubmissionStatus
    ) -> TutorialSubmission:
        logger.info(f"Updating tutorial submission: {tutorial_submission.id} with status: {status}")
        tutorial_submission.status = status
        tutorial_submission.save()
        logger.info(f"Tutorial submission updated: {tutorial_submission.id}")
        return tutorial_submission

    def bulk_update_status(self, filters: TutorialSubmissionListFilterSchema, status: TutorialSubmissionStatus) -> int:
        logger.info(f"Bulk updating tutorial submissions with status: {status}")
        submissions = self._tutorial_submission_retrieval_service.get_list(filters)
        return submissions.update(status=status)
