import logging

from django.conf import settings
from django.db import transaction
from injector import inject

from main.apps.gcp.services import GCPCloudTaskCreateService
from main.apps.internal_api.subscribers.schemas import PubSubEnvelopeSchema
from main.apps.internal_api.subscribers.services.pubsub_message_data_parser import PubSubMessageDataParser
from main.apps.internal_api.subscribers.types import TutorialSubmissionExecutionFinishedMessage
from main.apps.notifications.enums import NotificationLevel
from main.apps.notifications.schemas import NotificationCreateSchema
from main.apps.notifications.services import NotificationCreateService
from main.apps.tutorials.enums import TutorialSubmissionStatus
from main.apps.tutorials.models import TutorialSubmission
from main.apps.tutorials.services import TutorialSubmissionRetrievalService, TutorialSubmissionUpdateService


logger = logging.getLogger(__name__)


class TutorialSubmissionExecutionFinishedHandler:
    @inject
    def __init__(
        self,
        pubsub_message_data_parser: PubSubMessageDataParser,
        tutorial_submission_retrieval_service: TutorialSubmissionRetrievalService,
        tutorial_submission_update_service: TutorialSubmissionUpdateService,
        gcp_cloud_task_create_service: GCPCloudTaskCreateService,
        notification_create_service: NotificationCreateService,
    ):
        self._pubsub_message_data_parser = pubsub_message_data_parser
        self._tutorial_submission_retrieval_service = tutorial_submission_retrieval_service
        self._tutorial_submission_update_service = tutorial_submission_update_service
        self._gcp_cloud_task_create_service = gcp_cloud_task_create_service
        self._notification_create_service = notification_create_service

    def _enqueue_tutorial_submission_validate_task(self, tutorial_submission: TutorialSubmission) -> None:
        logger.info("Enqueuing tutorial submission validate task for tutorial submission: %s", tutorial_submission.id)
        self._gcp_cloud_task_create_service.create(
            queue_id=settings.GCP_TASKS_TUTORIAL_SUBMISSION_QUEUE_ID,
            url=f"{settings.INTERNAL_API_BASE_URL}/_internal-api/tasks/submissions/{tutorial_submission.id}/validate/",
            payload={
                "user_id": tutorial_submission.user_id,
            },
        )

    def _handle_execution_succeeded(
        self, tutorial_submission: TutorialSubmission, parsed_data: TutorialSubmissionExecutionFinishedMessage
    ) -> None:
        logger.info("Execution succeeded for tutorial submission: %s", tutorial_submission.id)
        tutorial_submission = self._tutorial_submission_update_service.update_status(
            tutorial_submission, TutorialSubmissionStatus.EXECUTION_SUCCEEDED, parsed_data.stdout
        )
        transaction.on_commit(lambda: self._enqueue_tutorial_submission_validate_task(tutorial_submission))

    def _handle_execution_failed(
        self, tutorial_submission: TutorialSubmission, parsed_data: TutorialSubmissionExecutionFinishedMessage
    ) -> None:
        logger.info("Execution failed for tutorial submission: %s", tutorial_submission.id)
        tutorial_submission = self._tutorial_submission_update_service.update_status(
            tutorial_submission, TutorialSubmissionStatus.EXECUTION_FAILED, parsed_data.stdout
        )
        self._notification_create_service.create(
            user_id=tutorial_submission.user_id,
            data=NotificationCreateSchema(
                text=f"Your submission for tutorial {tutorial_submission.tutorial.title} failed. Check the bug report for more details.",
                level=NotificationLevel.ERROR,
            ),
        )

    @transaction.atomic
    def handle(self, envelope: PubSubEnvelopeSchema) -> None:
        assert envelope.message.attributes["message_type"] == "tutorial_submission_execution_finished"

        # TODO: Publish a message to another pubsub topic, to populate update to frontend

        logger.info("Received message %s from subscription %s", envelope.message.message_id, envelope.subscription)
        parsed_data = self._pubsub_message_data_parser.parse_data(
            envelope.message.data, TutorialSubmissionExecutionFinishedMessage
        )
        tutorial_submission = self._tutorial_submission_retrieval_service.get_for_update_by_id(
            parsed_data.user_id, parsed_data.tutorial_submission_id
        )

        if parsed_data.exit_code == 0:
            return self._handle_execution_succeeded(tutorial_submission, parsed_data)
        else:
            return self._handle_execution_failed(tutorial_submission, parsed_data)
