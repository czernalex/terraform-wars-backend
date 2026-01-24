import logging
from uuid import UUID

from injector import inject
from django.utils.translation import gettext as _
from ninja.errors import ValidationError

from main.apps.core.exceptions import NotFoundError
from main.apps.providers.enums import ProviderUserProjectStatus
from main.apps.providers.models import Provider, ProviderUserProject
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

    def _validate_project_id_is_unique(self, user_id: UUID, provider_id: UUID, project_id: str) -> None:
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

    def _validate_provider_exists(self, provider_id: UUID) -> Provider:
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
        provider = self._validate_provider_exists(data.provider_id)
        self._validate_project_id_is_unique(user_id, data.provider_id, data.project_id)
        return CreateProviderUserProjectValidatedData(provider=provider)

    def validate_can_be_configured(self, provider_user_project: ProviderUserProject) -> None:
        if provider_user_project.status != ProviderUserProjectStatus.PENDING:
            logger.warning(
                "Provider user project %(provider_user_project_id)s is not in pending state. Skipping configuration.",
                {"provider_user_project_id": provider_user_project.id},
            )
            raise ValidationError(
                [
                    {
                        "loc": ["status"],
                        "msg": _("Provider user project is not in pending state"),
                        "type": "value_error",
                    }
                ]
            )

        if provider_user_project.configuration_attempts >= ProviderUserProject.MAX_CONFIGURATION_ATTEMPTS:
            logger.warning(
                "Provider user project %(provider_user_project_id)s has already reached the maximum number of configuration attempts. Skipping configuration.",
                {"provider_user_project_id": provider_user_project.id},
            )
            raise ValidationError(
                [
                    {
                        "loc": ["configuration_attempts"],
                        "msg": _(
                            "Provider user project has already reached the maximum number of configuration attempts"
                        ),
                        "type": "value_error",
                    }
                ]
            )
