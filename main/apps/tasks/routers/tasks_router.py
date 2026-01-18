from http import HTTPStatus
from uuid import UUID

from ninja import Router

from main.apps.tasks.services import TutorialSubmissionExecuteService
from main.di import injector
from main.apps.core.types import AuthedHttpRequest


tasks_router = Router()


@tasks_router.post(
    "/submissions/{tutorial_submission_id}/execute/",
    url_name="tutorial_submission_execute",
    response={HTTPStatus.ACCEPTED: None},
    description="Trigger a tutorial submission execution",
)
def execute_tutorial_submission(
    request: AuthedHttpRequest,
    tutorial_submission_id: UUID,
) -> None:
    tutorial_submission_execution_service = injector.get(TutorialSubmissionExecuteService)
    tutorial_submission_execution_service.execute(tutorial_submission_id)


@tasks_router.post(
    "/submissions/{tutorial_submission_id}/validate/",
    url_name="tutorial_submission_validate",
    response={HTTPStatus.ACCEPTED: None},
    description="Trigger a tutorial submission execution",
)
def validate_tutorial_submission(
    request: AuthedHttpRequest,
    tutorial_submission_id: UUID,
) -> None:
    pass
