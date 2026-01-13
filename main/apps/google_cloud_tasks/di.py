from django.conf import settings
from injector import Binder, Module, singleton, provider
from google.cloud import tasks_v2

from main.apps.google_cloud_tasks.services.cloud_task_create_service import CloudTaskCreateService


class GoogleCloudTasksModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(tasks_v2.CloudTasksClient, to=tasks_v2.CloudTasksClient, scope=singleton)

    @provider
    @singleton
    def provide_cloud_task_create_service(self, client: tasks_v2.CloudTasksClient) -> CloudTaskCreateService:
        return CloudTaskCreateService(
            client,
            settings.GCP_PROJECT_ID,
            settings.GCP_LOCATION,
            settings.GCP_SERVICE_ACCOUNT_EMAIL,
            settings.TASK_API_BASE_URL,
        )
