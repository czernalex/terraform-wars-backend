import logging
from uuid import UUID

from django.db import transaction
from injector import inject

from main.apps.providers.services.provider_user_project_retrieval_service import ProviderUserProjectRetrievalService


logger = logging.getLogger(__name__)


class ProviderUserProjectDeleteService:
    @inject
    def __init__(self, provider_user_project_retrieval_service: ProviderUserProjectRetrievalService):
        self._provider_user_project_retrieval_service = provider_user_project_retrieval_service

    @transaction.atomic
    def delete(self, user_id: UUID, provider_user_project_id: UUID) -> None:
        logger.info(
            "Deleting provider user project: %(provider_user_project_id)s",
            {"provider_user_project_id": provider_user_project_id},
        )
        provider_user_project = self._provider_user_project_retrieval_service.get_for_update_by_id(
            user_id, provider_user_project_id
        )
        # TODO: Validate, that no submissions that are associated with this project are being executed or validated
        provider_user_project.delete()
        logger.info(
            "Provider user project: %(provider_user_project_id)s successfully deleted",
            {"provider_user_project_id": provider_user_project_id},
        )
