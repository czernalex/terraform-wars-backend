from django.conf import settings
from injector import Binder, Module, singleton, provider
from google.cloud import tasks_v2, run_v2

from main.apps.gcp.services import (
    GCPCloudTaskCreateService,
    GCPCredentialsCreateService,
    GCPProjectCreateService,
    GCPProjectDeleteService,
    GCPServiceAccountCreateService,
    GCPServiceAccountImpersonationService,
    GCPServiceEnableService,
    GCPProjectIamRoleGrantService,
    GCPCloudRunJobInvokeService,
)


class GCPModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(tasks_v2.CloudTasksClient, to=tasks_v2.CloudTasksClient, scope=singleton)
        binder.bind(run_v2.JobsClient, to=run_v2.JobsClient, scope=singleton)
        binder.bind(GCPCredentialsCreateService, to=GCPCredentialsCreateService, scope=singleton)
        binder.bind(GCPProjectCreateService, to=GCPProjectCreateService, scope=singleton)
        binder.bind(GCPProjectDeleteService, to=GCPProjectDeleteService, scope=singleton)
        binder.bind(GCPServiceAccountCreateService, to=GCPServiceAccountCreateService, scope=singleton)
        binder.bind(GCPServiceAccountImpersonationService, to=GCPServiceAccountImpersonationService, scope=singleton)
        binder.bind(GCPServiceEnableService, to=GCPServiceEnableService, scope=singleton)
        binder.bind(GCPProjectIamRoleGrantService, to=GCPProjectIamRoleGrantService, scope=singleton)
        binder.bind(GCPCloudRunJobInvokeService, to=GCPCloudRunJobInvokeService, scope=singleton)

    @provider
    @singleton
    def provide_gcp_cloud_task_create_service(self, client: tasks_v2.CloudTasksClient) -> GCPCloudTaskCreateService:
        return GCPCloudTaskCreateService(
            client,
            settings.GCP_PROJECT_ID,
            settings.GCP_LOCATION,
            settings.GCP_SERVICE_ACCOUNT_EMAIL,
            settings.TASK_API_BASE_URL,
        )
