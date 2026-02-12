from http import HTTPStatus
from uuid import UUID

from django.db import models
from ninja import Query, Router
from ninja.pagination import paginate

from main.apps.core.schemas import NotFoundErrorSchema
from main.apps.providers.schemas import (
    CreateProviderUserProjectSchema,
    ProviderUserProjectDetailSchema,
    ProviderUserProjectListFilterSchema,
    ProviderUserProjectListSchema,
    UpdateProviderUserProjectSchema,
)
from main.apps.providers.services import (
    ProviderUserProjectCreateService,
    ProviderUserProjectDeleteService,
    ProviderUserProjectRetrievalService,
    ProviderUserProjectUpdateService,
)
from main.di import injector
from main.apps.core.types import AuthedHttpRequest
from main.apps.providers.models import ProviderUserProject


provider_user_projects_router = Router()


@provider_user_projects_router.get(
    "/",
    url_name="provider_user_project_list",
    response={HTTPStatus.OK: list[ProviderUserProjectListSchema]},
    description="List all provider user projects",
)
@paginate
def get_provider_user_project_list(
    request: AuthedHttpRequest,
    filters: Query[ProviderUserProjectListFilterSchema],
) -> models.QuerySet[ProviderUserProject]:
    filters.user_id = request.user.id
    provider_user_project_retrieval_service = injector.get(ProviderUserProjectRetrievalService)
    return provider_user_project_retrieval_service.get_list(filters)


@provider_user_projects_router.post(
    "/",
    url_name="provider_user_project_list",
    response={HTTPStatus.CREATED: ProviderUserProjectDetailSchema},
    description="Create a new provider user project for the authenticated user and the selected provider.",
)
def create_provider_user_project(
    request: AuthedHttpRequest,
    data: CreateProviderUserProjectSchema,
) -> ProviderUserProject:
    provider_user_project_create_service = injector.get(ProviderUserProjectCreateService)
    return provider_user_project_create_service.create(request.user.id, data)


@provider_user_projects_router.get(
    "/{provider_user_project_id}/",
    url_name="provider_user_project_detail",
    response={
        HTTPStatus.OK: ProviderUserProjectDetailSchema,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Get a provider user project by ID",
)
def get_provider_user_project_detail(
    request: AuthedHttpRequest,
    provider_user_project_id: UUID,
) -> ProviderUserProject:
    provider_user_project_retrieval_service = injector.get(ProviderUserProjectRetrievalService)
    return provider_user_project_retrieval_service.get_detail_by_id(request.user.id, provider_user_project_id)


@provider_user_projects_router.put(
    "/{provider_user_project_id}/",
    url_name="provider_user_project_detail",
    response={
        HTTPStatus.OK: ProviderUserProjectDetailSchema,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Update a provider user project by ID",
)
def update_provider_user_project(
    request: AuthedHttpRequest,
    provider_user_project_id: UUID,
    data: UpdateProviderUserProjectSchema,
) -> ProviderUserProject:
    provider_user_project_update_service = injector.get(ProviderUserProjectUpdateService)
    return provider_user_project_update_service.update(request.user.id, provider_user_project_id, data)


@provider_user_projects_router.delete(
    "/{provider_user_project_id}/",
    url_name="provider_user_project_detail",
    response={
        HTTPStatus.NO_CONTENT: None,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Delete a provider user project by ID",
)
def delete_provider_user_project(
    request: AuthedHttpRequest,
    provider_user_project_id: UUID,
) -> HTTPStatus:
    provider_user_project_delete_service = injector.get(ProviderUserProjectDeleteService)
    provider_user_project_delete_service.delete(request.user.id, provider_user_project_id)
    return HTTPStatus.NO_CONTENT
