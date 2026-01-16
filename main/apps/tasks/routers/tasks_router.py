from http import HTTPStatus
from uuid import UUID

from ninja import Router

from main.apps.tasks.services import TutorialSubmissionExecutionService
from main.di import injector
from main.apps.core.types import AuthedHttpRequest


tasks_router = Router()


@tasks_router.post(
    "/submissions/{tutorial_submission_id}/executions/",
    url_name="tutorial_submission_execution_list",
    response={HTTPStatus.OK: None},
    description="Trigger a tutorial submission execution",
)
def create_tutorial_submission_execution(
    request: AuthedHttpRequest,
    tutorial_submission_id: UUID,
) -> None:
    tutorial_submission_execution_service = injector.get(TutorialSubmissionExecutionService)
    tutorial_submission_execution_service.execute(tutorial_submission_id)
