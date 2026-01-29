from http import HTTPStatus
from uuid import UUID

from django.db import models
from ninja import Router

from main.apps.core.schemas import NotFoundErrorSchema
from main.di import injector
from main.apps.core.types import AuthedHttpRequest
from main.apps.tutorials.models import TutorialSubmission, TutorialSubmissionEvent
from main.apps.tutorials.schemas import (
    CreateTutorialSubmissionSchema,
    TutorialSubmissionDetailSchema,
    TutorialSubmissionEventListFilterSchema,
    TutorialSubmissionEventSchema,
)
from main.apps.tutorials.services import (
    TutorialSubmissionCreateService,
    TutorialSubmissionEventRetrievalService,
    TutorialSubmissionRetrievalService,
)


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
    tutorial_submission_retrieval_service = injector.get(TutorialSubmissionRetrievalService)
    return tutorial_submission_retrieval_service.get_detail_by_id(request.user.id, tutorial_submission_id)


@tutorial_submissions_router.get(
    "/{tutorial_submission_id}/events/",
    url_name="tutorial_submission_detail_events_list",
    response={
        HTTPStatus.OK: list[TutorialSubmissionEventSchema],
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Get the detail of a tutorial submission for the authenticated user and the selected tutorial.",
)
def get_tutorial_submission_events_list(
    request: AuthedHttpRequest,
    tutorial_submission_id: UUID,
    filters: TutorialSubmissionEventListFilterSchema,
) -> models.QuerySet[TutorialSubmissionEvent]:
    filters.user_id = request.user.id
    filters.tutorial_submission_id = tutorial_submission_id
    tutorial_submission_event_retrieval_service = injector.get(TutorialSubmissionEventRetrievalService)
    return tutorial_submission_event_retrieval_service.get_list(filters)
