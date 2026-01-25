import logging

from django.conf import settings
from django.urls import reverse_lazy
from injector import inject

from main.apps.providers.enums import ProviderUserProjectStatus
from main.apps.providers.models import ProviderUserProject
from main.apps.providers.schemas import ProviderUserProjectListFilterSchema
from main.apps.providers.services import ProviderUserProjectRetrievalService
from main.apps.gcp.services import GCPCloudTaskCreateService


logger = logging.getLogger(__name__)


class ProviderUserProjectConfigureScheduler:
    @inject
    def __init__(
        self,
        provider_user_project_retrieval_service: ProviderUserProjectRetrievalService,
        gcp_cloud_task_create_service: GCPCloudTaskCreateService,
    ):
        self._provider_user_project_retrieval_service = provider_user_project_retrieval_service
        self._gcp_cloud_task_create_service = gcp_cloud_task_create_service

    def _enqueue_configuration_task(self, provider_user_project: ProviderUserProject) -> None:
        logger.info(
            "Enqueuing configuration task for provider user project: %(provider_user_project_id)s",
            {
                "provider_user_project_id": provider_user_project.id,
            },
        )
        task_url = f"{settings.INTERNAL_API_BASE_URL}{reverse_lazy('terraform-wars-internal-api:provider_user_project_configuration_list', kwargs={'provider_user_project_id': provider_user_project.id})}"
        self._gcp_cloud_task_create_service.create(
            settings.GCP_TASKS_PROVIDER_USER_PROJECT_CONFIGURATION_QUEUE_ID,
            task_url,
            payload={
                "user_id": provider_user_project.user_id,
            },
        )

    def schedule(self) -> None:
        filters = ProviderUserProjectListFilterSchema(
            status=ProviderUserProjectStatus.PENDING,
            configuration_attempts=ProviderUserProject.MAX_CONFIGURATION_ATTEMPTS,
        )
        provider_user_projects = self._provider_user_project_retrieval_service.get_list(filters)
        for provider_user_project in provider_user_projects:
            self._enqueue_configuration_task(provider_user_project)
