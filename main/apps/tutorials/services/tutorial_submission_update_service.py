import logging
from typing import Optional

from main.apps.tutorials.enums import TutorialSubmissionStatus
from main.apps.tutorials.models.tutorial_submission import TutorialSubmission


logger = logging.getLogger(__name__)


class TutorialSubmissionUpdateService:
    def update_status(
        self, tutorial_submission: TutorialSubmission, status: TutorialSubmissionStatus, result: Optional[str] = None
    ) -> TutorialSubmission:
        logger.info(f"Updating tutorial submission: {tutorial_submission.id} with status: {status}")
        tutorial_submission.status = status
        if result is not None:
            tutorial_submission.result = result
        tutorial_submission.save()
        logger.info(f"Tutorial submission updated: {tutorial_submission.id}")
        return tutorial_submission
