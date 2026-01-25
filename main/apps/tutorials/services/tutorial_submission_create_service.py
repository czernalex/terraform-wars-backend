import logging
from uuid import UUID

from django.conf import settings
from django.db import transaction
from django.urls import reverse_lazy
from injector import inject
from ninja.errors import ValidationError

from main.apps.core.exceptions import NotFoundError
from main.apps.gcp.services import GCPCloudTaskCreateService
from main.apps.tutorials.models import TutorialSubmission
from main.apps.tutorials.schemas import CreateTutorialSubmissionSchema
from main.apps.tutorials.services.tutorial_retrieval_service import TutorialRetrievalService
from main.apps.tutorials.services.tutorial_validation_service import TutorialValidationService
from main.apps.users.models import User


logger = logging.getLogger(__name__)


class TutorialSubmissionCreateService:
    @inject
    def __init__(
        self,
        tutorial_retrieval_service: TutorialRetrievalService,
        tutorial_validation_service: TutorialValidationService,
        gcp_cloud_task_create_service: GCPCloudTaskCreateService,
    ) -> None:
        self._tutorial_retrieval_service = tutorial_retrieval_service
        self._tutorial_validation_service = tutorial_validation_service
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

    def _create_tutorial_submission(self, user_id: UUID, tutorial_id: UUID, code: str) -> TutorialSubmission:
        logger.info(
            "Creating tutorial submission for user: %(user_id)s and tutorial: %(tutorial_id)s",
            {
                "user_id": user_id,
                "tutorial_id": tutorial_id,
            },
        )
        return TutorialSubmission.objects.create(
            tutorial_id=tutorial_id,
            user_id=user_id,
            code=code,
        )

    @transaction.atomic
    def create(self, user: User, data: CreateTutorialSubmissionSchema) -> TutorialSubmission:
        try:
            tutorial = self._tutorial_retrieval_service.get_detail_by_id(data.tutorial_id)
        except NotFoundError as error:
            logger.warning("Tutorial not found: %(tutorial_id)s", {"tutorial_id": data.tutorial_id})
            raise ValidationError(
                [
                    {
                        "loc": ["tutorial_id"],
                        "msg": str(error),
                        "type": "value_error",
                    }
                ]
            )

        self._tutorial_validation_service.validate_accepts_submissions(tutorial)

        tutorial_submission = self._create_tutorial_submission(user.id, tutorial.id, data.code)
        self._enqueue_tutorial_submission_task(tutorial_submission)
        return tutorial_submission
