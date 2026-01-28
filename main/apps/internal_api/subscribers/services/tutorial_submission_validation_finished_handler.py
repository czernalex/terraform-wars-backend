import logging

from django.db import transaction
from injector import inject

from main.apps.gcp.services import GCPCloudTaskCreateService
from main.apps.internal_api.subscribers.schemas import PubSubEnvelopeSchema
from main.apps.internal_api.subscribers.services.pubsub_message_data_parser import PubSubMessageDataParser
from main.apps.internal_api.subscribers.types import TutorialSubmissionValidationFinishedMessage
from main.apps.tutorials.enums import TutorialSubmissionStatus
from main.apps.tutorials.models import TutorialSubmission
from main.apps.tutorials.services import TutorialSubmissionRetrievalService, TutorialSubmissionUpdateService


logger = logging.getLogger(__name__)


class TutorialSubmissionValidationFinishedHandler:
    @inject
    def __init__(
        self,
        pubsub_message_data_parser: PubSubMessageDataParser,
        tutorial_submission_retrieval_service: TutorialSubmissionRetrievalService,
        tutorial_submission_update_service: TutorialSubmissionUpdateService,
        gcp_cloud_task_create_service: GCPCloudTaskCreateService,
    ):
        self._pubsub_message_data_parser = pubsub_message_data_parser
        self._tutorial_submission_retrieval_service = tutorial_submission_retrieval_service
        self._tutorial_submission_update_service = tutorial_submission_update_service
        self._gcp_cloud_task_create_service = gcp_cloud_task_create_service

    def _handle_validation_succeeded(self, tutorial_submission: TutorialSubmission) -> None:
        logger.info("Validation succeeded for tutorial submission: %s", tutorial_submission.id)
        tutorial_submission = self._tutorial_submission_update_service.update_status(
            tutorial_submission, TutorialSubmissionStatus.SUCCEEDED
        )

    def _handle_validation_failed(self, tutorial_submission: TutorialSubmission) -> None:
        logger.info("Validation failed for tutorial submission: %s", tutorial_submission.id)
        tutorial_submission = self._tutorial_submission_update_service.update_status(
            tutorial_submission, TutorialSubmissionStatus.FAILED
        )

    @transaction.atomic
    def handle(self, envelope: PubSubEnvelopeSchema) -> None:
        assert envelope.message.attributes["message_type"] == "tutorial_submission_validation_finished"

        logger.info("Received message %s from subscription %s", envelope.message.message_id, envelope.subscription)

        parsed_data = self._pubsub_message_data_parser.parse_data(
            envelope.message.data, TutorialSubmissionValidationFinishedMessage
        )
        tutorial_submission = self._tutorial_submission_retrieval_service.get_for_update_by_id(
            parsed_data.user_id, parsed_data.tutorial_submission_id
        )

        if parsed_data.exit_code == 0:
            return self._handle_validation_succeeded(tutorial_submission)
        else:
            return self._handle_validation_failed(tutorial_submission)
