from http import HTTPStatus

from django.db import models
from ninja import Query, Router
from ninja.pagination import paginate

from main.apps.tutorials.services import TutorialCreateService, TutorialRetrievalService
from main.di import injector
from main.apps.core.schemas import NotFoundErrorSchema
from main.apps.core.types import AuthedHttpRequest
from main.apps.tutorials.models import Tutorial
from main.apps.tutorials.schemas import (
    CreateTutorialSchema,
    TutorialDetailSchema,
    TutorialListFilterSchema,
    TutorialListSchema,
)


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
    return tutorial_retrieval_service.get_list(filters)


@tutorials_router.post(
    "/",
    url_name="tutorial_list",
    response={HTTPStatus.CREATED: TutorialDetailSchema},
    description="Create new tutorial",
)
def create_tutorial(
    request: AuthedHttpRequest,
    data: CreateTutorialSchema,
) -> models.QuerySet[Tutorial]:
    tutorial_create_service = injector.get(TutorialCreateService)
    return tutorial_create_service.create(request.user.id, data)


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
    return tutorial_retrieval_service.get_detail_by_slug(tutorial_slug)
