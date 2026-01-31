import asyncio
import logging
import uuid

import msgspec
from google.cloud import pubsub_v1
from injector import inject

from main.apps.gcp.services import GCPPubSubSubscribeService, GCPPubSubSubscriptionCreateService
from main.apps.tutorials.types import TutorialSubmissionEventMessage
from main.apps.tutorials.services.tutorial_submission_event_hub_service import TutorialSubmissionEventHubService


logger = logging.getLogger(__name__)


class TutorialSubmissionEventStreamSetupService:
    @inject
    def __init__(
        self,
        gcp_pubsub_subscription_create_service: GCPPubSubSubscriptionCreateService,
        gcp_pubsub_subscribe_service: GCPPubSubSubscribeService,
        tutorial_submission_event_hub_service: TutorialSubmissionEventHubService,
        gcp_project_id: str,
    ):
        self._gcp_pubsub_subscription_create_service = gcp_pubsub_subscription_create_service
        self._gcp_pubsub_subscribe_service = gcp_pubsub_subscribe_service
        self._tutorial_submission_event_hub_service = tutorial_submission_event_hub_service
        self._gcp_project_id = gcp_project_id

    def _generate_subscription_name(self) -> str:
        return f"tutorial-submission-events-sub-{uuid.uuid4()}"

    def setup(self, loop: asyncio.AbstractEventLoop) -> None:
        subscription = self._gcp_pubsub_subscription_create_service.create(
            project_id=self._gcp_project_id,
            topic_name="tutorial-submission-events",
            subscription_name=self._generate_subscription_name(),
        )
        logger.info(f"Created tutorial submission events subscription: {subscription.name}")

        def callback(message: "pubsub_v1.subscriber.message.Message") -> None:
            tutorial_submission_event_message = msgspec.json.decode(message.data, type=TutorialSubmissionEventMessage)

            loop.call_soon_threadsafe(
                lambda: asyncio.create_task(
                    self._tutorial_submission_event_hub_service.abroadcast(
                        tutorial_submission_event_message.user_id,
                        tutorial_submission_event_message.tutorial_submission_id,
                        tutorial_submission_event_message.tutorial_submission_event_id,
                    )
                )
            )

            message.ack()

        self._gcp_pubsub_subscribe_service.subscribe(
            subscription_path=subscription.name,
            callback=callback,
        )
