from http import HTTPStatus
from uuid import UUID

from ninja import Router

from main.apps.tutorials.services import TutorialStepSubmissionRetrievalService
from main.di import injector
from main.apps.core.types import AuthedHttpRequest


tasks_router = Router()


@tasks_router.post(
    "/submissions/{tutorial_step_submission_id}/executions/",
    url_name="tutorial_step_submission_execution_list",
    response={HTTPStatus.OK: None},
    description="Trigger a tutorial step submission execution",
)
def create_tutorial_step_submission_execution(
    request: AuthedHttpRequest,
    tutorial_step_submission_id: UUID,
) -> None:
    tutorial_step_submission_retrieval_service = injector.get(TutorialStepSubmissionRetrievalService)
    tutorial_step_submission = tutorial_step_submission_retrieval_service.get_detail_by_id(tutorial_step_submission_id)
