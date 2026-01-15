from http import HTTPStatus
from uuid import UUID

from django.db import models
from ninja import Query, Router
from ninja.pagination import paginate

from main.di import injector
from main.apps.core.types import AuthedHttpRequest
from main.apps.core.schemas import NotFoundErrorSchema
from main.apps.tutorials.models import TutorialProject
from main.apps.tutorials.schemas import (
    CreateTutorialProjectSchema,
    TutorialProjectDetailSchema,
    TutorialProjectListFilterSchema,
    TutorialProjectListSchema,
)
from main.apps.tutorials.services import (
    TutorialProjectCreateService,
    TutorialProjectRetrievalService,
    TutorialProjectDeleteService,
)


tutorial_projects_router = Router()


@tutorial_projects_router.get(
    "/",
    url_name="tutorial_project_list",
    response={HTTPStatus.OK: list[TutorialProjectListSchema]},
    description="List all tutorial projects for the authenticated user",
)
@paginate
def get_tutorial_project_list(
    request: AuthedHttpRequest, filters: Query[TutorialProjectListFilterSchema]
) -> models.QuerySet[TutorialProject]:
    tutorial_project_retrieval_service = injector.get(TutorialProjectRetrievalService)
    return tutorial_project_retrieval_service.get_list(request.user, filters)


@tutorial_projects_router.post(
    "/",
    url_name="tutorial_project_list",
    response={HTTPStatus.CREATED: TutorialProjectDetailSchema},
    description="Create a new tutorial project for the authenticated user and the selected tutorial.",
)
def create_tutorial_project(request: AuthedHttpRequest, data: CreateTutorialProjectSchema) -> TutorialProject:
    tutorial_project_create_service = injector.get(TutorialProjectCreateService)
    return tutorial_project_create_service.create(request.user, data)


@tutorial_projects_router.get(
    "/{tutorial_project_id}/",
    url_name="tutorial_project_detail",
    response={
        HTTPStatus.OK: TutorialProjectDetailSchema,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Get the detail of a tutorial project for the authenticated user and the selected tutorial.",
)
def get_tutorial_project_detail(request: AuthedHttpRequest, tutorial_project_id: UUID) -> TutorialProject:
    tutorial_project_retrieval_service = injector.get(TutorialProjectRetrievalService)
    return tutorial_project_retrieval_service.get_detail_by_id(request.user, tutorial_project_id)


@tutorial_projects_router.delete(
    "/{tutorial_project_id}/",
    url_name="tutorial_project_detail",
    response={
        HTTPStatus.NO_CONTENT: None,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Delete a tutorial project for the authenticated user and the selected tutorial.",
)
def delete_tutorial_project(request: AuthedHttpRequest, tutorial_project_id: UUID) -> None:
    tutorial_project_delete_service = injector.get(TutorialProjectDeleteService)
    return tutorial_project_delete_service.delete(request.user, tutorial_project_id)


@tutorial_projects_router.delete(
    "/{tutorial_project_id}/resources/",
    url_name="tutorial_project_resources_list",
    response={
        HTTPStatus.NO_CONTENT: None,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Delete the resources of a tutorial project for the authenticated user and the selected tutorial.",
)
def delete_tutorial_project_resources(request: AuthedHttpRequest, tutorial_project_id: UUID) -> None:
    tutorial_project_delete_service = injector.get(TutorialProjectDeleteService)
    return tutorial_project_delete_service.destroy_resources(request.user, tutorial_project_id)
