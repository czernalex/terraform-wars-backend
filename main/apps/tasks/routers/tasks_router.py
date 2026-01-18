from http import HTTPStatus
from uuid import UUID

from django.http import HttpRequest
from ninja import Router

from main.apps.tasks.services import TutorialSubmissionExecuteService, TutorialSubmissionValidateService
from main.di import injector


tasks_router = Router()


# TODO: We should return a response schema which will allow us to track the status of the execution and validation processes


@tasks_router.post(
    "/submissions/{tutorial_submission_id}/execute/",
    url_name="tutorial_submission_execute",
    response={HTTPStatus.ACCEPTED: None},
    description="Trigger a tutorial submission execution",
)
def execute_tutorial_submission(
    request: HttpRequest,
    tutorial_submission_id: UUID,
) -> None:
    tutorial_submission_execution_service = injector.get(TutorialSubmissionExecuteService)
    tutorial_submission_execution_service.execute(tutorial_submission_id)


@tasks_router.post(
    "/submissions/{tutorial_submission_id}/validate/",
    url_name="tutorial_submission_validate",
    response={HTTPStatus.ACCEPTED: None},
    description="Trigger a tutorial submission validation",
)
def validate_tutorial_submission(
    request: HttpRequest,
    tutorial_submission_id: UUID,
) -> None:
    tutorial_submission_validate_service = injector.get(TutorialSubmissionValidateService)
    tutorial_submission_validate_service.validate(tutorial_submission_id)
