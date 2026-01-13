from http import HTTPStatus

from django.db import models
from ninja import Query, Router
from ninja.pagination import paginate

from main.di import injector
from main.apps.core.schemas import NotFoundErrorSchema
from main.apps.core.types import AuthedHttpRequest
from main.apps.tutorials.models import Tutorial, TutorialStep
from main.apps.tutorials.schemas import (
    TutorialDetailSchema,
    TutorialListFilterSchema,
    TutorialListSchema,
    TutorialStepDetailSchema,
    TutorialStepListSchema,
)
from main.apps.tutorials.services.tutorial_retrieval_service import TutorialRetrievalService
from main.apps.tutorials.services.tutorial_step_retrieval_service import TutorialStepRetrievalService


tutorials_router = Router()


@tutorials_router.get(
    "/",
    url_name="tutorial_list",
    response={HTTPStatus.OK: list[TutorialListSchema]},
    description="List all tutorials",
)
@paginate
def get_tutorial_list(
    request: AuthedHttpRequest,
    filters: Query[TutorialListFilterSchema],
) -> models.QuerySet[Tutorial]:
    tutorial_retrieval_service = injector.get(TutorialRetrievalService)
    return tutorial_retrieval_service.get_tutorial_list(filters)


@tutorials_router.get(
    "/{tutorial_slug}/",
    url_name="tutorial_detail",
    response={
        HTTPStatus.OK: TutorialDetailSchema,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Get a tutorial by slug",
)
def get_tutorial_detail(
    request: AuthedHttpRequest,
    tutorial_slug: str,
) -> Tutorial:
    tutorial_retrieval_service = injector.get(TutorialRetrievalService)
    return tutorial_retrieval_service.get_tutorial_detail_by_slug(tutorial_slug)


@tutorials_router.get(
    "/{tutorial_slug}/steps/",
    url_name="tutorial_step_list",
    response={HTTPStatus.OK: list[TutorialStepListSchema]},
    description="List all steps for a tutorial",
)
def get_tutorial_step_list(
    request: AuthedHttpRequest,
    tutorial_slug: str,
) -> models.QuerySet[TutorialStepListSchema]:
    tutorial_step_retrieval_service = injector.get(TutorialStepRetrievalService)
    return tutorial_step_retrieval_service.get_tutorial_step_list(tutorial_slug)


@tutorials_router.get(
    "/{tutorial_slug}/steps/{tutorial_step_slug}/",
    url_name="tutorial_step_detail",
    response={HTTPStatus.OK: TutorialStepDetailSchema, HTTPStatus.NOT_FOUND: NotFoundErrorSchema},
    description="Get a tutorial step by slug",
)
def get_tutorial_step_detail(
    request: AuthedHttpRequest,
    tutorial_slug: str,
    tutorial_step_slug: str,
) -> TutorialStep:
    tutorial_step_retrieval_service = injector.get(TutorialStepRetrievalService)
    return tutorial_step_retrieval_service.get_tutorial_step_detail_by_slug(tutorial_slug, tutorial_step_slug)
