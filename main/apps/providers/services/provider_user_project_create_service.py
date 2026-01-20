import logging
from uuid import UUID

from django.db import transaction
from injector import inject

from main.apps.providers.models import ProviderUserProject
from main.apps.providers.services.provider_user_project_validation_service import ProviderUserProjectValidationService
from main.apps.providers.schemas import CreateProviderUserProjectSchema

logger = logging.getLogger(__name__)


class ProviderUserProjectCreateService:
    @inject
    def __init__(
        self,
        provider_user_project_validation_service: ProviderUserProjectValidationService,
    ):
        self._provider_user_project_validation_service = provider_user_project_validation_service

    def _create_provider_user_project(
        self, user_id: UUID, data: CreateProviderUserProjectSchema
    ) -> ProviderUserProject:
        return ProviderUserProject.objects.create(
            provider_id=data.provider_id,
            user_id=user_id,
            project_id=data.project_id,
            name=data.name,
            description=data.description,
            config_data=data.config_data,
        )

    @transaction.atomic
    def create(self, user_id: UUID, data: CreateProviderUserProjectSchema) -> ProviderUserProject:
        logger.info(
            "Creating provider user project for user: %(user_id)s and provider: %(provider_id)s",
            {"user_id": user_id, "provider_id": data.provider_id},
        )
        self._provider_user_project_validation_service.validate_create_data(data)
        provider_user_project = self._create_provider_user_project(user_id, data)
        logger.info(
            "Provider user project created: %(provider_user_project_id)s",
            {"provider_user_project_id": provider_user_project.id},
        )
        return provider_user_project
