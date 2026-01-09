from http import HTTPStatus
from uuid import UUID
from ninja import Router

from main.di import injector
from main.apps.core.types import AuthedHttpRequest
from main.apps.tutorials.models import TutorialStepSubmission
from main.apps.tutorials.schemas import CreateTutorialStepSubmissionSchema, TutorialStepSubmissionDetailSchema
from main.apps.tutorials.services.tutorial_step_submission_service import TutorialStepSubmissionService


tutorial_step_submissions_router = Router()


@tutorial_step_submissions_router.post(
    "/",
    url_name="tutorial_step_submission_list",
    response={HTTPStatus.CREATED: None},
)
def create_tutorial_step_submission(
    request: AuthedHttpRequest,
    data: CreateTutorialStepSubmissionSchema,
) -> TutorialStepSubmission:
    tutorial_step_submission_service = injector.get(TutorialStepSubmissionService)
    return tutorial_step_submission_service.create_tutorial_step_submission(request.user, data)


@tutorial_step_submissions_router.get(
    "/{tutorial_step_submission_id}/",
    url_name="tutorial_step_submission_detail",
    response={HTTPStatus.OK: TutorialStepSubmissionDetailSchema},
)
def get_tutorial_step_submission_detail(
    request: AuthedHttpRequest,
    tutorial_step_submission_id: UUID,
) -> TutorialStepSubmission:
    tutorial_step_submission_service = injector.get(TutorialStepSubmissionService)
    return tutorial_step_submission_service.get_tutorial_step_submission_detail(tutorial_step_submission_id)
