import logging
from uuid import UUID

from django.db import transaction
from injector import inject

from main.apps.tutorials.services.tutorial_retrieval_service import TutorialRetrievalService
from main.apps.tutorials.services.tutorial_validation_service import TutorialValidationService


logger = logging.getLogger(__name__)


class TutorialDeleteService:
    @inject
    def __init__(
        self,
        tutorial_retrieval_service: TutorialRetrievalService,
        tutorial_validation_service: TutorialValidationService,
    ):
        self._tutorial_retrieval_service = tutorial_retrieval_service
        self._tutorial_validation_service = tutorial_validation_service

    @transaction.atomic
    def delete(self, user_id: UUID, tutorial_id: UUID) -> None:
        logger.info(f"Deleting tutorial: {tutorial_id}")
        tutorial = self._tutorial_retrieval_service.get_for_update_by_id(user_id, tutorial_id)
        self._tutorial_validation_service.validate_can_be_deleted(tutorial)
        tutorial.delete()
        logger.info(f"Tutorial deleted: {tutorial_id}")
