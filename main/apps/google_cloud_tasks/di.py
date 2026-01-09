from django.conf import settings
from injector import Binder, Module, singleton, provider
from google.cloud import tasks_v2

from main.apps.google_cloud_tasks.services.create_http_task_service import CreateHttpTaskService


class GoogleCloudTasksModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(tasks_v2.CloudTasksClient, to=tasks_v2.CloudTasksClient, scope=singleton)

    @provider
    @singleton
    def provide_create_http_task_service(self, client: tasks_v2.CloudTasksClient) -> CreateHttpTaskService:
        return CreateHttpTaskService(client, settings.GCP_PROJECT_ID, settings.GCP_LOCATION)
