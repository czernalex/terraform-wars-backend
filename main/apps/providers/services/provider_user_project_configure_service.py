import logging
from uuid import UUID

from django.db import transaction
from injector import inject

from main.apps.providers.enums import ProviderUserProjectStatus
from main.apps.providers.exceptions import ProviderUserProjectConfigurationError
from main.apps.providers.models import ProviderUserProject
from main.apps.providers.schemas import UpdateProviderUserProjectSchema
from main.apps.providers.services.provider_user_project_retrieval_service import ProviderUserProjectRetrievalService
from main.apps.providers.services.provider_user_project_configurator_factory import (
    ProviderUserProjectConfiguratorFactory,
)
from main.apps.providers.services.provider_user_project_update_service import ProviderUserProjectUpdateService
from main.apps.providers.services.provider_user_project_validation_service import ProviderUserProjectValidationService

logger = logging.getLogger(__name__)


class ProviderUserProjectConfigureService:
    @inject
    def __init__(
        self,
        provider_user_project_retrieval_service: ProviderUserProjectRetrievalService,
        provider_user_project_validation_service: ProviderUserProjectValidationService,
        provider_user_project_update_service: ProviderUserProjectUpdateService,
        provider_user_project_configurator_factory: ProviderUserProjectConfiguratorFactory,
    ):
        self._provider_user_project_retrieval_service = provider_user_project_retrieval_service
        self._provider_user_project_validation_service = provider_user_project_validation_service
        self._provider_user_project_update_service = provider_user_project_update_service
        self._provider_user_project_configurator_factory = provider_user_project_configurator_factory

    def _handle_failed_configuration_attempt(
        self, provider_user_project: ProviderUserProject, error: ProviderUserProjectConfigurationError
    ) -> ProviderUserProject:
        return self._provider_user_project_update_service.update_with_data(
            provider_user_project,
            UpdateProviderUserProjectSchema(
                name=provider_user_project.name,
                description=provider_user_project.description,
                status=ProviderUserProjectStatus.FAILED
                if provider_user_project.configuration_attempts >= ProviderUserProject.MAX_CONFIGURATION_ATTEMPTS
                else ProviderUserProjectStatus.PENDING,
                configuration_attempts=provider_user_project.configuration_attempts + 1,
                configuration_error=str(error),
            ),
        )

    def _handle_successful_configuration_attempt(
        self, provider_user_project: ProviderUserProject
    ) -> ProviderUserProject:
        return self._provider_user_project_update_service.update_with_data(
            provider_user_project,
            UpdateProviderUserProjectSchema(
                name=provider_user_project.name,
                description=provider_user_project.description,
                status=ProviderUserProjectStatus.CONFIGURED,
                configuration_attempts=provider_user_project.configuration_attempts + 1,
                configuration_error="",
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
        self._provider_user_project_validation_service.validate_can_be_configured(provider_user_project)
        provider_user_project_configurator = self._provider_user_project_configurator_factory.get_configurator(
            provider_user_project
        )

        try:
            provider_user_project = provider_user_project_configurator.configure(provider_user_project)
        except ProviderUserProjectConfigurationError as error:
            return self._handle_failed_configuration_attempt(provider_user_project, error)

        provider_user_project = self._handle_successful_configuration_attempt(provider_user_project)
        logger.info(
            "Provider user project configured successfully: %(provider_user_project_id)s",
            {"provider_user_project_id": provider_user_project_id},
        )
        return provider_user_project
