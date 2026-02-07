import logging
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from injector import inject

from main.apps.notifications.enums import NotificationLevel
from main.apps.notifications.schemas import NotificationCreateSchema
from main.apps.notifications.services.notification_create_service import NotificationCreateService
from main.apps.tutorials.enums import TutorialSubmissionStatus
from main.apps.tutorials.models import TutorialSubmission
from main.apps.tutorials.schemas import CreateTutorialSubmissionEventSchema, TutorialSubmissionListFilterSchema
from main.apps.tutorials.services import TutorialSubmissionEventCreateService, TutorialSubmissionRetrievalService
from main.apps.tutorials.services.tutorial_submission_update_service import TutorialSubmissionUpdateService

logger = logging.getLogger(__name__)


class TutorialSubmissionReconciliationService:
    @inject
    def __init__(
        self,
        tutorial_submission_retrieval_service: TutorialSubmissionRetrievalService,
        tutorial_submission_update_service: TutorialSubmissionUpdateService,
        tutorial_submission_event_create_service: TutorialSubmissionEventCreateService,
        notification_create_service: NotificationCreateService,
    ):
        self._tutorial_submission_retrieval_service = tutorial_submission_retrieval_service
        self._tutorial_submission_update_service = tutorial_submission_update_service
        self._tutorial_submission_event_create_service = tutorial_submission_event_create_service
        self._notification_create_service = notification_create_service

    @transaction.atomic
    def _reconcile_submission(
        self, submission: TutorialSubmission, status: TutorialSubmissionStatus, error: str
    ) -> None:
        self._tutorial_submission_update_service.update_status(submission, status)
        self._tutorial_submission_event_create_service.create(
            submission.id,
            CreateTutorialSubmissionEventSchema(
                event_status=status,
                exit_code=1,
                stdout=error,
                error=error,
            ),
        )
        self._notification_create_service.create(
            submission.user_id,
            NotificationCreateSchema(
                text=f"Your submission for tutorial {submission.tutorial.title} failed. Check the bug report for more details.",
                level=NotificationLevel.ERROR,
            ),
        )
        logger.info(f"Reconciled submission: {submission.id}")

    def _reconcile_execution_failed_submissions(self) -> None:
        filters = TutorialSubmissionListFilterSchema(
            status=[
                TutorialSubmissionStatus.PENDING,
                TutorialSubmissionStatus.EXECUTING,
            ],
            created_at=timezone.now() - timedelta(hours=2),
        )
        submissions = self._tutorial_submission_retrieval_service.get_list(filters)

        for submission in submissions:
            self._reconcile_submission(
                submission,
                TutorialSubmissionStatus.EXECUTION_FAILED,
                "Failed to execute the submission within the timeout.",
            )

    def _reconcile_validation_failed_submissions(self) -> None:
        filters = TutorialSubmissionListFilterSchema(
            status=[
                TutorialSubmissionStatus.EXECUTION_SUCCEEDED,
                TutorialSubmissionStatus.VALIDATING,
            ],
            created_at=timezone.now() - timedelta(hours=2),
        )
        submissions = self._tutorial_submission_retrieval_service.get_list(filters)

        for submission in submissions:
            self._reconcile_submission(
                submission,
                TutorialSubmissionStatus.FAILED,
                "Failed to validate the submission within the timeout.",
            )

    @transaction.atomic
    def reconcile(self) -> None:
        self._reconcile_execution_failed_submissions()
        self._reconcile_validation_failed_submissions()
