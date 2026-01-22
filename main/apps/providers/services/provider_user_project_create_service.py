import logging
from uuid import UUID

from django.db import transaction
from injector import inject

from main.apps.providers.models import Provider, ProviderUserProject
from main.apps.providers.services.provider_user_project_config_data_formatter_service_factory import (
    ProviderUserProjectConfigDataFormatterServiceFactory,
)
from main.apps.providers.services.provider_user_project_validation_service import ProviderUserProjectValidationService
from main.apps.providers.schemas import CreateProviderUserProjectSchema

logger = logging.getLogger(__name__)


class ProviderUserProjectCreateService:
    @inject
    def __init__(
        self,
        provider_user_project_validation_service: ProviderUserProjectValidationService,
        provider_user_project_config_data_formatter_service_factory: ProviderUserProjectConfigDataFormatterServiceFactory,
    ):
        self._provider_user_project_validation_service = provider_user_project_validation_service
        self._provider_user_project_config_data_formatter_service_factory = (
            provider_user_project_config_data_formatter_service_factory
        )

    def _create_provider_user_project(
        self, user_id: UUID, provider: Provider, data: CreateProviderUserProjectSchema
    ) -> ProviderUserProject:
        formatter_service = self._provider_user_project_config_data_formatter_service_factory.get_formatter_service(
            provider
        )
        config_data = formatter_service.format(provider, data)
        return ProviderUserProject.objects.create(
            provider_id=data.provider_id,
            user_id=user_id,
            project_id=data.project_id,
            name=data.display_name,
            config_data=config_data,
        )

    @transaction.atomic
    def create(self, user_id: UUID, data: CreateProviderUserProjectSchema) -> ProviderUserProject:
        logger.info(
            "Creating provider user project for user: %(user_id)s and provider: %(provider_id)s",
            {"user_id": user_id, "provider_id": data.provider_id},
        )
        validated_data = self._provider_user_project_validation_service.validate_create_data(data)
        provider_user_project = self._create_provider_user_project(user_id, validated_data.provider, data)
        logger.info(
            "Provider user project created: %(provider_user_project_id)s",
            {"provider_user_project_id": provider_user_project.id},
        )
        return provider_user_project
