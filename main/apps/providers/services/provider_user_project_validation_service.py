import logging
from uuid import UUID

from injector import inject
from ninja.errors import ValidationError

from main.apps.core.exceptions import NotFoundError
from main.apps.providers.models import Provider
from main.apps.providers.schemas import CreateProviderUserProjectSchema
from main.apps.providers.services.provider_retrieval_service import ProviderRetrievalService
from main.apps.providers.services.provider_user_project_config_data_validation_service_factory import (
    ProviderUserProjectConfigDataValidationServiceFactory,
)


logger = logging.getLogger(__name__)


class ProviderUserProjectValidationService:
    @inject
    def __init__(
        self,
        provider_retrieval_service: ProviderRetrievalService,
        provider_user_project_config_data_validation_service_factory: ProviderUserProjectConfigDataValidationServiceFactory,
    ):
        self._provider_retrieval_service = provider_retrieval_service
        self._provider_user_project_config_data_validation_service_factory = (
            provider_user_project_config_data_validation_service_factory
        )

    def _validate_config_data_for_provider(self, provider: Provider, data: CreateProviderUserProjectSchema) -> None:
        validation_service = self._provider_user_project_config_data_validation_service_factory.get_validation_service(
            provider
        )
        validation_service.validate(provider, data)

    def validate_provider_exists(self, provider_id: UUID) -> Provider:
        try:
            return self._provider_retrieval_service.get_detail_by_id(provider_id)
        except NotFoundError as error:
            logger.warning("Provider not found: %(provider_id)s", {"provider_id": provider_id})
            raise ValidationError(
                [
                    {
                        "loc": ["provider_id"],
                        "msg": str(error),
                        "type": "value_error",
                    }
                ]
            ) from error

    def validate_create_data(self, data: CreateProviderUserProjectSchema) -> None:
        provider = self.validate_provider_exists(data.provider_id)
        self._validate_config_data_for_provider(provider, data)
