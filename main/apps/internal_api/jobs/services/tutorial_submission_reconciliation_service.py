import logging
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from injector import inject

from main.apps.tutorials.enums import TutorialSubmissionStatus
from main.apps.tutorials.schemas import TutorialSubmissionListFilterSchema
from main.apps.tutorials.services.tutorial_submission_update_service import TutorialSubmissionUpdateService

logger = logging.getLogger(__name__)


class TutorialSubmissionReconciliationService:
    @inject
    def __init__(self, tutorial_submission_update_service: TutorialSubmissionUpdateService):
        self._tutorial_submission_update_service = tutorial_submission_update_service

    def _reconcile_execution_failed_submissions(self) -> None:
        filters = TutorialSubmissionListFilterSchema(
            status=[
                TutorialSubmissionStatus.PENDING,
                TutorialSubmissionStatus.EXECUTING,
            ],
            created_at=timezone.now() - timedelta(hours=2),
        )
        updated_count = self._tutorial_submission_update_service.bulk_update_status(
            filters, TutorialSubmissionStatus.EXECUTION_FAILED
        )
        logger.info(f"Reconciled {updated_count} execution failed submissions")

    def _reconcile_validation_failed_submissions(self) -> None:
        filters = TutorialSubmissionListFilterSchema(
            status=[
                TutorialSubmissionStatus.EXECUTION_SUCCEEDED,
                TutorialSubmissionStatus.VALIDATING,
            ],
            created_at=timezone.now() - timedelta(hours=2),
        )
        updated_count = self._tutorial_submission_update_service.bulk_update_status(
            filters, TutorialSubmissionStatus.FAILED
        )
        logger.info(f"Reconciled {updated_count} validation failed submissions")

    @transaction.atomic
    def reconcile(self) -> None:
        self._reconcile_execution_failed_submissions()
        self._reconcile_validation_failed_submissions()
