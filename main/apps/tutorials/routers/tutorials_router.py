from http import HTTPStatus
from uuid import UUID

from django.db import models
from ninja import Query, Router
from ninja.pagination import paginate

from main.apps.tutorials.services import (
    TutorialCreateService,
    TutorialDeleteService,
    TutorialRetrievalService,
    TutorialUpdateService,
)
from main.di import injector
from main.apps.core.schemas import NotFoundErrorSchema
from main.apps.core.types import AuthedHttpRequest
from main.apps.tutorials.models import Tutorial
from main.apps.tutorials.schemas import (
    CreateTutorialSchema,
    PartialUpdateTutorialSchema,
    TutorialDetailSchema,
    TutorialListFilterSchema,
    TutorialListSchema,
    UpdateTutorialSchema,
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
    return tutorial_retrieval_service.get_list(filters, request.user.id)


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


@tutorials_router.put(
    "/{uuid:tutorial_id}/",
    url_name="tutorial_detail",
    response={
        HTTPStatus.OK: TutorialDetailSchema,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Update a tutorial by ID",
)
def update_tutorial(
    request: AuthedHttpRequest,
    tutorial_id: UUID,
    data: UpdateTutorialSchema,
) -> Tutorial:
    tutorial_update_service = injector.get(TutorialUpdateService)
    return tutorial_update_service.update(request.user.id, tutorial_id, data)


@tutorials_router.patch(
    "/{uuid:tutorial_id}/",
    url_name="tutorial_detail",
    response={
        HTTPStatus.OK: TutorialDetailSchema,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Partially update a tutorial by ID",
)
def partial_update_tutorial(
    request: AuthedHttpRequest,
    tutorial_id: UUID,
    data: PartialUpdateTutorialSchema,
) -> Tutorial:
    tutorial_update_service = injector.get(TutorialUpdateService)
    return tutorial_update_service.partial_update(request.user.id, tutorial_id, data)


@tutorials_router.delete(
    "/{uuid:tutorial_id}/",
    url_name="tutorial_detail",
    response={
        HTTPStatus.NO_CONTENT: None,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Archive a tutorial by ID",
)
def delete_tutorial(
    request: AuthedHttpRequest,
    tutorial_id: UUID,
) -> None:
    tutorial_delete_service = injector.get(TutorialDeleteService)
    return tutorial_delete_service.delete(request.user.id, tutorial_id)


@tutorials_router.get(
    "/{str:tutorial_slug}/",
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
    return tutorial_retrieval_service.get_detail_by_slug(tutorial_slug, request.user.id)
