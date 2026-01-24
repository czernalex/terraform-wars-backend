import logging
from uuid import UUID

from django.db import transaction
from injector import inject

from main.apps.providers.models import ProviderUserProject
from main.apps.providers.schemas import UpdateProviderUserProjectSchema
from main.apps.providers.services.provider_user_project_retrieval_service import ProviderUserProjectRetrievalService

logger = logging.getLogger(__name__)


class ProviderUserProjectUpdateService:
    @inject
    def __init__(self, provider_user_project_retrieval_service: ProviderUserProjectRetrievalService):
        self._provider_user_project_retrieval_service = provider_user_project_retrieval_service

    def update_with_data(
        self, provider_user_project: ProviderUserProject, data: UpdateProviderUserProjectSchema
    ) -> ProviderUserProject:
        provider_user_project.name = data.name
        provider_user_project.description = data.description
        provider_user_project.status = data.status
        provider_user_project.configuration_attempts = data.configuration_attempts
        provider_user_project.configuration_error = data.configuration_error
        provider_user_project.save()
        return provider_user_project

    @transaction.atomic
    def update(
        self,
        user_id: UUID,
        provider_user_project_id: UUID,
        data: UpdateProviderUserProjectSchema,
    ) -> ProviderUserProject:
        logger.info(
            "Updating provider user project: %(provider_user_project_id)s",
            {"provider_user_project_id": provider_user_project_id},
        )
        provider_user_project = self._provider_user_project_retrieval_service.get_for_update_by_id(
            user_id, provider_user_project_id
        )
        provider_user_project = self.update_with_data(provider_user_project, data)
        logger.info(
            "Provider user project: %(provider_user_project_id)s successfully updated",
            {"provider_user_project_id": provider_user_project_id},
        )
        return provider_user_project
