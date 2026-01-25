import asyncio
import msgspec
import uuid

from injector import inject

from main.apps.gcp.services import GCPPubSubSubscriptionCreateService, GCPPubSubSubscribeService
from main.apps.notifications.services.notification_hub_service import NotificationHubService
from main.apps.notifications.types import NotificationMessage


class NotificationStreamSetupService:
    @inject
    def __init__(
        self,
        gcp_pubsub_subscription_create_service: GCPPubSubSubscriptionCreateService,
        gcp_pubsub_subscribe_service: GCPPubSubSubscribeService,
        notification_hub_service: NotificationHubService,
        gcp_project_id: str,
    ):
        self._gcp_pubsub_subscription_create_service = gcp_pubsub_subscription_create_service
        self._gcp_pubsub_subscribe_service = gcp_pubsub_subscribe_service
        self._notification_hub_service = notification_hub_service
        self._gcp_project_id = gcp_project_id

    def _generate_subscription_name(self) -> str:
        return f"notifications-sub-{uuid.uuid4()}"

    def setup(self, loop: asyncio.AbstractEventLoop) -> None:
        subscription = self._gcp_pubsub_subscription_create_service.create(
            project_id=self._gcp_project_id,
            topic_name="notifications",
            subscription_name=self._generate_subscription_name(),
        )

        def callback(message) -> None:
            notification_message = msgspec.json.decode(message.data, type=NotificationMessage)

            loop.call_soon_threadsafe(
                lambda: asyncio.create_task(
                    self._notification_hub_service.abroadcast(
                        notification_message.user_id, notification_message.notification_id
                    )
                )
            )

            message.ack()

        self._gcp_pubsub_subscribe_service.subscribe(
            subscription_path=subscription.name,
            callback=callback,
        )
