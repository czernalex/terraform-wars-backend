import logging
from uuid import UUID

from injector import inject
from ninja.errors import ValidationError

from main.apps.core.exceptions import NotFoundError
from main.apps.providers.models import Provider
from main.apps.providers.schemas import CreateProviderUserProjectSchema
from main.apps.providers.services.provider_retrieval_service import ProviderRetrievalService


logger = logging.getLogger(__name__)


class ProviderUserProjectValidationService:
    @inject
    def __init__(
        self,
        provider_retrieval_service: ProviderRetrievalService,
    ):
        self._provider_retrieval_service = provider_retrieval_service

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

    def validate_create_data(self, data: CreateProviderUserProjectSchema) -> Provider:
        return self.validate_provider_exists(data.provider_id)
