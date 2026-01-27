import logging
from uuid import UUID

from django.db import transaction
from injector import inject

from main.apps.tutorials.models import Tutorial
from main.apps.tutorials.schemas import PartialUpdateTutorialSchema, UpdateTutorialSchema
from main.apps.tutorials.services.tutorial_retrieval_service import TutorialRetrievalService
from main.apps.tutorials.services.tutorial_validation_service import TutorialValidationService
from main.apps.tutorials.types import CreateOrUpdateTutorialValidatedData


logger = logging.getLogger(__name__)


class TutorialUpdateService:
    @inject
    def __init__(
        self,
        tutorial_retrieval_service: TutorialRetrievalService,
        tutorial_validation_service: TutorialValidationService,
    ):
        self._tutorial_retrieval_service = tutorial_retrieval_service
        self._tutorial_validation_service = tutorial_validation_service

    def _update_tutorial(self, tutorial: Tutorial, validated_data: CreateOrUpdateTutorialValidatedData) -> Tutorial:
        tutorial.save()
        logger.info(f"Tutorial updated: {tutorial.id}")
        if not validated_data.tag_ids:
            return tutorial
        tutorial.tags.set(validated_data.tag_ids)
        logger.info(f"Assigned {len(validated_data.tag_ids)} tags for tutorial {tutorial.id}")
        return tutorial

    def _partial_update_tutorial(self, tutorial: Tutorial, data: PartialUpdateTutorialSchema) -> Tutorial:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(tutorial, field, value)
        tutorial.save()
        logger.info(f"Tutorial partially updated: {tutorial.id}")
        return tutorial

    @transaction.atomic
    def update(self, user_id: UUID, tutorial_id: UUID, data: UpdateTutorialSchema) -> Tutorial:
        logger.info(f"Updating tutorial: {tutorial_id}, user_id: {user_id}")
        tutorial = self._tutorial_retrieval_service.get_for_update_by_id(user_id, tutorial_id)
        validated_data = self._tutorial_validation_service.validate_update_data(tutorial, data)
        return self._update_tutorial(tutorial, validated_data)

    @transaction.atomic
    def partial_update(self, user_id: UUID, tutorial_id: UUID, data: PartialUpdateTutorialSchema) -> Tutorial:
        logger.info(f"Partial updating tutorial: {tutorial_id}, user_id: {user_id}")
        tutorial = self._tutorial_retrieval_service.get_for_update_by_id(user_id, tutorial_id)
        self._tutorial_validation_service.validate_partial_update_data(tutorial, data)
        return self._partial_update_tutorial(tutorial, data)
