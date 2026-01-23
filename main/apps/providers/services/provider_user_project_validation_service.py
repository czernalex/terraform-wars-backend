import logging
from uuid import UUID

from injector import inject
from django.utils.translation import gettext as _
from ninja.errors import ValidationError

from main.apps.core.exceptions import NotFoundError
from main.apps.providers.models import Provider
from main.apps.providers.schemas import CreateProviderUserProjectSchema, ProviderUserProjectListFilterSchema
from main.apps.providers.services.provider_retrieval_service import ProviderRetrievalService
from main.apps.providers.services.provider_user_project_retrieval_service import ProviderUserProjectRetrievalService
from main.apps.providers.types import CreateProviderUserProjectValidatedData


logger = logging.getLogger(__name__)


class ProviderUserProjectValidationService:
    @inject
    def __init__(
        self,
        provider_retrieval_service: ProviderRetrievalService,
        provider_user_project_retrieval_service: ProviderUserProjectRetrievalService,
    ):
        self._provider_retrieval_service = provider_retrieval_service
        self._provider_user_project_retrieval_service = provider_user_project_retrieval_service

    def validate_project_id_is_unique(self, user_id: UUID, provider_id: UUID, project_id: str) -> None:
        filters = ProviderUserProjectListFilterSchema(user_id=user_id, provider_id=provider_id, project_id=project_id)
        if self._provider_user_project_retrieval_service.get_list(filters):
            raise ValidationError(
                [
                    {
                        "loc": ["project_id"],
                        "msg": _("Project ID is already associated with another provider user project"),
                        "type": "value_error",
                    }
                ]
            )

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

    def validate_create_data(
        self, user_id: UUID, data: CreateProviderUserProjectSchema
    ) -> CreateProviderUserProjectValidatedData:
        provider = self.validate_provider_exists(data.provider_id)
        self.validate_project_id_is_unique(user_id, data.provider_id, data.project_id)
        return CreateProviderUserProjectValidatedData(provider=provider)
