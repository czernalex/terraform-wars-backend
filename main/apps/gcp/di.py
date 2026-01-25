from django.conf import settings
from injector import Binder, Module, singleton, provider
from google.cloud import tasks_v2, run_v2, pubsub_v1

from main.apps.gcp.services import (
    GCPCloudTaskCreateService,
    GCPOAuth2CredentialsCreateService,
    GCPProjectBillingInfoGetService,
    GCPProjectSearchService,
    GCPPubSubPublishService,
    GCPPubSubSubscribeService,
    GCPPubSubSubscriptionCreateService,
    GCPServiceAccountImpersonationService,
    GCPServiceEnableService,
    GCPProjectIamRoleGrantService,
    GCPCloudRunJobInvokeService,
)


class GCPModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(tasks_v2.CloudTasksClient, to=tasks_v2.CloudTasksClient, scope=singleton)
        binder.bind(run_v2.JobsClient, to=run_v2.JobsClient, scope=singleton)
        binder.bind(pubsub_v1.SubscriberClient, to=pubsub_v1.SubscriberClient, scope=singleton)
        binder.bind(pubsub_v1.PublisherClient, to=pubsub_v1.PublisherClient, scope=singleton)
        binder.bind(GCPOAuth2CredentialsCreateService, to=GCPOAuth2CredentialsCreateService, scope=singleton)
        binder.bind(GCPServiceAccountImpersonationService, to=GCPServiceAccountImpersonationService, scope=singleton)
        binder.bind(GCPServiceEnableService, to=GCPServiceEnableService, scope=singleton)
        binder.bind(GCPProjectIamRoleGrantService, to=GCPProjectIamRoleGrantService, scope=singleton)
        binder.bind(GCPProjectSearchService, to=GCPProjectSearchService, scope=singleton)
        binder.bind(GCPProjectBillingInfoGetService, to=GCPProjectBillingInfoGetService, scope=singleton)
        binder.bind(GCPPubSubSubscribeService, to=GCPPubSubSubscribeService, scope=singleton)
        binder.bind(GCPPubSubSubscriptionCreateService, to=GCPPubSubSubscriptionCreateService, scope=singleton)

    @provider
    @singleton
    def provide_gcp_cloud_task_create_service(self, client: tasks_v2.CloudTasksClient) -> GCPCloudTaskCreateService:
        return GCPCloudTaskCreateService(
            client,
            settings.GCP_PROJECT_ID,
            settings.GCP_REGION,
            settings.GCP_SERVICE_ACCOUNT_EMAIL,
            settings.INTERNAL_API_BASE_URL,
        )

    @provider
    @singleton
    def provide_gcp_cloud_run_job_invoke_service(self, client: run_v2.JobsClient) -> GCPCloudRunJobInvokeService:
        return GCPCloudRunJobInvokeService(
            client,
            settings.GCP_PROJECT_ID,
            settings.GCP_REGION,
        )

    @provider
    @singleton
    def provide_gcp_pubsub_publish_service(self, client: pubsub_v1.PublisherClient) -> GCPPubSubPublishService:
        return GCPPubSubPublishService(
            client,
            settings.GCP_PROJECT_ID,
        )
