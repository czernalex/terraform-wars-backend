import logging
from uuid import UUID

from django.conf import settings
from django.db import transaction
from django.urls import reverse_lazy
from injector import inject

from main.apps.gcp.services import GCPCloudTaskCreateService
from main.apps.tutorials.models import TutorialSubmission
from main.apps.tutorials.schemas import CreateTutorialSubmissionSchema
from main.apps.tutorials.services.tutorial_submission_validation_service import TutorialSubmissionValidationService
from main.apps.tutorials.types import CreateTutorialSubmissionValidatedData
from main.apps.users.models import User


logger = logging.getLogger(__name__)


class TutorialSubmissionCreateService:
    @inject
    def __init__(
        self,
        tutorial_submission_validation_service: TutorialSubmissionValidationService,
        gcp_cloud_task_create_service: GCPCloudTaskCreateService,
    ) -> None:
        self._tutorial_submission_validation_service = tutorial_submission_validation_service
        self._gcp_cloud_task_create_service = gcp_cloud_task_create_service

    def _enqueue_tutorial_submission_task(self, tutorial_submission: TutorialSubmission) -> None:
        transaction.on_commit(
            lambda: self._gcp_cloud_task_create_service.create(
                queue_id=settings.GCP_TASKS_TUTORIAL_SUBMISSION_QUEUE_ID,
                url=f"{settings.INTERNAL_API_BASE_URL}{
                    reverse_lazy(
                        'terraform-wars-internal-api:tutorial_submission_execute',
                        kwargs={'tutorial_submission_id': tutorial_submission.id},
                    )
                }",
            )
        )

    def _create_tutorial_submission(
        self, user_id: UUID, validated_data: CreateTutorialSubmissionValidatedData
    ) -> TutorialSubmission:
        logger.info(
            "Creating tutorial submission for user: %(user_id)s and tutorial: %(tutorial_id)s and provider user project: %(provider_user_project_id)s",
            {
                "user_id": user_id,
                "tutorial_id": validated_data.tutorial.id,
                "provider_user_project_id": validated_data.provider_user_project.id,
            },
        )
        tutorial_submission = TutorialSubmission.objects.create(
            user_id=user_id,
            tutorial_id=validated_data.tutorial.id,
            provider_user_project_id=validated_data.provider_user_project.id,
            code=validated_data.code,
        )
        logger.info(f"Tutorial submission created: {tutorial_submission.id}")
        return tutorial_submission

    @transaction.atomic
    def create(self, user: User, data: CreateTutorialSubmissionSchema) -> TutorialSubmission:
        validated_data = self._tutorial_submission_validation_service.validate_create_data(user.id, data)
        tutorial_submission = self._create_tutorial_submission(user.id, validated_data)
        self._enqueue_tutorial_submission_task(tutorial_submission)
        return tutorial_submission
