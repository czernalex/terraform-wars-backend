from django.conf import settings
from django.db import transaction
from injector import inject
from ninja.errors import ValidationError

from main.apps.core.exceptions import NotFoundError
from main.apps.google_cloud_tasks.services.cloud_task_create_service import CloudTaskCreateService
from main.apps.tutorials.models import TutorialStepSubmission
from main.apps.tutorials.schemas import CreateTutorialStepSubmissionSchema
from main.apps.tutorials.services.tutorial_retrieval_service import TutorialRetrievalService
from main.apps.tutorials.services.tutorial_step_retrieval_service import TutorialStepRetrievalService
from main.apps.users.models import User


class TutorialStepSubmissionService:
    @inject
    def __init__(
        self,
        tutorial_retrieval_service: TutorialRetrievalService,
        tutorial_step_retrieval_service: TutorialStepRetrievalService,
        cloud_task_create_service: CloudTaskCreateService,
    ) -> None:
        self._tutorial_retrieval_service = tutorial_retrieval_service
        self._tutorial_step_retrieval_service = tutorial_step_retrieval_service
        self._cloud_task_create_service = cloud_task_create_service

    def _enqueue_tutorial_step_submission_task(self, tutorial_step_submission: TutorialStepSubmission) -> None:
        transaction.on_commit(
            lambda: self._cloud_task_create_service.create(
                queue_id=settings.GCP_TASKS_TUTORIAL_SUBMISSION_QUEUE_ID,
                url=f"{settings.TASK_API_BASE_URL}/tasks-api/tasks/submissions/{tutorial_step_submission.id}/executions/",
            )
        )

    @transaction.atomic
    def create_tutorial_step_submission(
        self, user: User, data: CreateTutorialStepSubmissionSchema
    ) -> TutorialStepSubmission:
        try:
            tutorial_step = self._tutorial_step_retrieval_service.get_tutorial_step_detail_by_id(data.tutorial_step_id)
        except NotFoundError as error:
            raise ValidationError(
                [
                    {
                        "loc": ["username"],
                        "msg": str(error),
                        "type": "value_error",
                    }
                ]
            ) from error

        tutorial_step_submission = TutorialStepSubmission.objects.create(
            tutorial_step=tutorial_step,
            user=user,
            code=data.code,
        )
        self._enqueue_tutorial_step_submission_task(tutorial_step_submission)
        return tutorial_step_submission
