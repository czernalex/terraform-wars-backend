import logging
from uuid import UUID

import msgspec
from django.db import transaction
from injector import inject

from main.apps.gcp.services import GCPPubSubPublishService
from main.apps.tutorials.models import TutorialSubmissionEvent
from main.apps.tutorials.schemas import CreateTutorialSubmissionEventSchema
from main.apps.tutorials.types import TutorialSubmissionEventMessage


logger = logging.getLogger(__name__)


class TutorialSubmissionEventCreateService:
    @inject
    def __init__(self, gcp_pubsub_publish_service: GCPPubSubPublishService):
        self._gcp_pubsub_publish_service = gcp_pubsub_publish_service

    def _dispatch_tutorial_submission_event(self, tutorial_submission_event: TutorialSubmissionEvent) -> None:
        message = TutorialSubmissionEventMessage(
            user_id=tutorial_submission_event.tutorial_submission.user_id,
            tutorial_submission_id=tutorial_submission_event.tutorial_submission_id,
            tutorial_submission_event_id=tutorial_submission_event.id,
        )
        transaction.on_commit(
            lambda: self._gcp_pubsub_publish_service.publish("tutorial-submission-events", msgspec.json.encode(message))
        )

    @transaction.atomic
    def create(
        self,
        tutorial_submission_id: UUID,
        data: CreateTutorialSubmissionEventSchema,
    ) -> TutorialSubmissionEvent:
        tutorial_submission_event = TutorialSubmissionEvent.objects.create(
            tutorial_submission_id=tutorial_submission_id,
            event_status=data.event_status,
            exit_code=data.exit_code,
            stdout=data.stdout,
            error=data.error or "",
        )
        self._dispatch_tutorial_submission_event(tutorial_submission_event)
        logger.info("Tutorial submission event created: %s", tutorial_submission_event.id)
        return tutorial_submission_event
