import logging
from uuid import UUID

from django.db import transaction
from injector import inject

from main.apps.tutorials.schemas import CreateTutorialSchema
from main.apps.tutorials.models import Tutorial
from main.apps.tutorials.services.tutorial_validation_service import TutorialValidationService
from main.apps.tutorials.types import CreateOrUpdateTutorialValidatedData


logger = logging.getLogger(__name__)


class TutorialCreateService:
    @inject
    def __init__(self, tutorial_validation_service: TutorialValidationService):
        self._tutorial_validation_service = tutorial_validation_service

    def _create_tutorial(
        self,
        user_id: UUID,
        data: CreateTutorialSchema,
        validated_data: CreateOrUpdateTutorialValidatedData,
    ) -> Tutorial:
        tutorial = Tutorial.objects.create(
            provider_id=validated_data.provider.id,
            author_id=user_id,
            title=data.title,
            slug=validated_data.slug,
            description=data.description,
            assignment=data.assignment,
            difficulty=data.difficulty,
            validation_script=data.validation_script,
            code_template=data.code_template,
            status=validated_data.status,
        )
        logger.info(f"Tutorial created: {tutorial.id}")

        if not validated_data.tag_ids:
            return tutorial

        tutorial.tags.set(validated_data.tag_ids)
        logger.info(f"Assigned {len(validated_data.tag_ids)} tags for tutorial {tutorial.id}")
        return tutorial

    @transaction.atomic
    def create(self, user_id: UUID, data: CreateTutorialSchema) -> Tutorial:
        validated_data = self._tutorial_validation_service.validate_create_data(data)
        return self._create_tutorial(user_id, data, validated_data)
