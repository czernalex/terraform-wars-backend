from django.conf import settings
from injector import Binder, Module, singleton, provider

from main.apps.gcp.services import GCPPubSubSubscriptionCreateService, GCPPubSubSubscribeService
from main.apps.notifications.services import (
    NotificationCreateService,
    NotificationHubService,
    NotificationRetrievalService,
    NotificationStreamService,
    NotificationUpdateService,
    NotificationEventBuilder,
    NotificationStreamSetupService,
)


class NotificationsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(NotificationRetrievalService, to=NotificationRetrievalService, scope=singleton)
        binder.bind(NotificationCreateService, to=NotificationCreateService, scope=singleton)
        binder.bind(NotificationUpdateService, to=NotificationUpdateService, scope=singleton)
        binder.bind(NotificationStreamService, to=NotificationStreamService, scope=singleton)
        binder.bind(NotificationEventBuilder, to=NotificationEventBuilder, scope=singleton)
        binder.bind(NotificationHubService, to=NotificationHubService, scope=singleton)

    @provider
    @singleton
    def provide_notification_stream_setup_service(
        self,
        gcp_pubsub_subscription_create_service: GCPPubSubSubscriptionCreateService,
        gcp_pubsub_subscribe_service: GCPPubSubSubscribeService,
        notification_hub_service: NotificationHubService,
    ) -> NotificationStreamSetupService:
        return NotificationStreamSetupService(
            gcp_pubsub_subscription_create_service=gcp_pubsub_subscription_create_service,
            gcp_pubsub_subscribe_service=gcp_pubsub_subscribe_service,
            notification_hub_service=notification_hub_service,
            gcp_project_id=settings.GCP_PROJECT_ID,
        )
