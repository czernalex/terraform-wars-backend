from http import HTTPStatus
from uuid import UUID

from ninja import Router

from main.apps.core.schemas import NotFoundErrorSchema
from main.di import injector
from main.apps.core.types import AuthedHttpRequest
from main.apps.tutorials.models import TutorialSubmission
from main.apps.tutorials.schemas import (
    CreateTutorialSubmissionSchema,
    TutorialSubmissionDetailSchema,
)
from main.apps.tutorials.services.tutorial_submission_create_service import TutorialSubmissionCreateService


tutorial_submissions_router = Router()


@tutorial_submissions_router.post(
    "/",
    url_name="tutorial_submission_list",
    response={HTTPStatus.CREATED: None},
    description="Create a new tutorial submission for the authenticated user and the selected tutorial.",
)
def create_tutorial_submission(
    request: AuthedHttpRequest,
    data: CreateTutorialSubmissionSchema,
) -> TutorialSubmission:
    tutorial_submission_create_service = injector.get(TutorialSubmissionCreateService)
    return tutorial_submission_create_service.create(request.user, data)


@tutorial_submissions_router.get(
    "/{tutorial_submission_id}/",
    url_name="tutorial_submission_detail",
    response={
        HTTPStatus.OK: TutorialSubmissionDetailSchema,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Get the detail of a tutorial submission for the authenticated user and the selected tutorial.",
)
def get_tutorial_submission_detail(
    request: AuthedHttpRequest,
    tutorial_submission_id: UUID,
) -> TutorialSubmission:
    pass
