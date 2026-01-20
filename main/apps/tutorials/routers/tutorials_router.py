from http import HTTPStatus

from django.db import models
from ninja import Query, Router
from ninja.pagination import paginate

from main.di import injector
from main.apps.core.schemas import NotFoundErrorSchema
from main.apps.core.types import AuthedHttpRequest
from main.apps.tutorials.models import Tutorial
from main.apps.tutorials.schemas import (
    TutorialDetailSchema,
    TutorialListFilterSchema,
    TutorialListSchema,
)
from main.apps.tutorials.services.tutorial_retrieval_service import TutorialRetrievalService


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
    return tutorial_retrieval_service.get_list(request.user, filters)


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
