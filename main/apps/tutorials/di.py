from django.conf import settings
from injector import Binder, Module, singleton, provider

from main.apps.gcp.services import GCPPubSubSubscribeService, GCPPubSubSubscriptionCreateService
from main.apps.tutorials.services import (
    TutorialCreateService,
    TutorialDeleteService,
    TutorialRetrievalService,
    TutorialReviewRetrievalService,
    TutorialSubmissionEventCreateService,
    TutorialSubmissionEventEventBuilder,
    TutorialSubmissionEventHubService,
    TutorialSubmissionEventRetrievalService,
    TutorialSubmissionEventStreamService,
    TutorialSubmissionEventStreamSetupService,
    TutorialSubmissionRetrievalService,
    TutorialSubmissionCreateService,
    TutorialSubmissionUpdateService,
    TutorialSubmissionValidationService,
    TutorialTagRetrievalService,
    TutorialUpdateService,
    TutorialValidationService,
)


class TutorialsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(TutorialRetrievalService, to=TutorialRetrievalService, scope=singleton)
        binder.bind(TutorialCreateService, to=TutorialCreateService, scope=singleton)
        binder.bind(TutorialUpdateService, to=TutorialUpdateService, scope=singleton)
        binder.bind(TutorialDeleteService, to=TutorialDeleteService, scope=singleton)
        binder.bind(TutorialTagRetrievalService, to=TutorialTagRetrievalService, scope=singleton)
        binder.bind(TutorialSubmissionRetrievalService, to=TutorialSubmissionRetrievalService, scope=singleton)
        binder.bind(TutorialSubmissionCreateService, to=TutorialSubmissionCreateService, scope=singleton)
        binder.bind(TutorialValidationService, to=TutorialValidationService, scope=singleton)
        binder.bind(TutorialSubmissionValidationService, to=TutorialSubmissionValidationService, scope=singleton)
        binder.bind(TutorialReviewRetrievalService, to=TutorialReviewRetrievalService, scope=singleton)
        binder.bind(TutorialSubmissionUpdateService, to=TutorialSubmissionUpdateService, scope=singleton)
        binder.bind(TutorialSubmissionEventStreamService, to=TutorialSubmissionEventStreamService, scope=singleton)
        binder.bind(
            TutorialSubmissionEventRetrievalService, to=TutorialSubmissionEventRetrievalService, scope=singleton
        )
        binder.bind(TutorialSubmissionEventEventBuilder, to=TutorialSubmissionEventEventBuilder, scope=singleton)
        binder.bind(TutorialSubmissionEventHubService, to=TutorialSubmissionEventHubService, scope=singleton)
        binder.bind(TutorialSubmissionEventCreateService, to=TutorialSubmissionEventCreateService, scope=singleton)

    @provider
    @singleton
    def provide_tutorial_submission_event_stream_setup_service(
        self,
        gcp_pubsub_subscription_create_service: GCPPubSubSubscriptionCreateService,
        gcp_pubsub_subscribe_service: GCPPubSubSubscribeService,
        tutorial_submission_event_hub_service: TutorialSubmissionEventHubService,
    ) -> TutorialSubmissionEventStreamSetupService:
        return TutorialSubmissionEventStreamSetupService(
            gcp_pubsub_subscription_create_service=gcp_pubsub_subscription_create_service,
            gcp_pubsub_subscribe_service=gcp_pubsub_subscribe_service,
            tutorial_submission_event_hub_service=tutorial_submission_event_hub_service,
            gcp_project_id=settings.GCP_PROJECT_ID,
        )
