import logging
from uuid import UUID

from django.db import transaction
from injector import inject

from main.apps.providers.enums import ProviderUserProjectStatus
from main.apps.providers.models import ProviderUserProject
from main.apps.providers.schemas import UpdateProviderUserProjectSchema
from main.apps.providers.services.provider_user_project_retrieval_service import ProviderUserProjectRetrievalService
from main.apps.providers.services.provider_user_project_configurator_factory import (
    ProviderUserProjectConfiguratorFactory,
)
from main.apps.providers.services.provider_user_project_update_service import ProviderUserProjectUpdateService

logger = logging.getLogger(__name__)


class ProviderUserProjectConfigureService:
    @inject
    def __init__(
        self,
        provider_user_project_retrieval_service: ProviderUserProjectRetrievalService,
        provider_user_project_update_service: ProviderUserProjectUpdateService,
        provider_user_project_configurator_factory: ProviderUserProjectConfiguratorFactory,
    ):
        self._provider_user_project_retrieval_service = provider_user_project_retrieval_service
        self._provider_user_project_update_service = provider_user_project_update_service
        self._provider_user_project_configurator_factory = provider_user_project_configurator_factory

    def _handle_failed_configuration(self, provider_user_project: ProviderUserProject) -> None:
        logger.warning(
            "Provider user project has reached the maximum number of configuration attempts: %(provider_user_project_id)s",
            {"provider_user_project_id": provider_user_project.id},
        )
        self._provider_user_project_update_service.update_with_data(
            provider_user_project,
            UpdateProviderUserProjectSchema(
                name=provider_user_project.name,
                description=provider_user_project.description,
                status=ProviderUserProjectStatus.FAILED,
                configuration_attempts=provider_user_project.configuration_attempts + 1,
            ),
        )

    @transaction.atomic
    def configure(self, user_id: UUID, provider_user_project_id: UUID) -> ProviderUserProject:
        logger.info(
            "Configuring provider user project: %(provider_user_project_id)s",
            {"provider_user_project_id": provider_user_project_id},
        )
        provider_user_project = self._provider_user_project_retrieval_service.get_for_update_by_id(
            user_id,
            provider_user_project_id,
        )

        if provider_user_project.status != ProviderUserProjectStatus.PENDING:
            logger.warning(
                "Provider user project is not pending: %(provider_user_project_id)s",
                {"provider_user_project_id": provider_user_project_id},
            )
            return

        if provider_user_project.configuration_attempts >= ProviderUserProject.MAX_CONFIGURATION_ATTEMPTS:
            return self._handle_failed_configuration(provider_user_project)

        provider_user_project_configurator = self._provider_user_project_configurator_factory.get_configurator(
            provider_user_project
        )
        provider_user_project = provider_user_project_configurator.configure(provider_user_project)
        self._provider_user_project_update_service.update_with_data(
            provider_user_project,
            UpdateProviderUserProjectSchema(
                name=provider_user_project.name,
                description=provider_user_project.description,
                status=ProviderUserProjectStatus.CONFIGURED,
                configuration_attempts=provider_user_project_configurator.configuration_attempts + 1,
            ),
        )
        logger.info(
            "Provider user project configured successfully: %(provider_user_project_id)s",
            {"provider_user_project_id": provider_user_project_id},
        )
        return provider_user_project
