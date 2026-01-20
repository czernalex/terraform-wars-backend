from http import HTTPStatus
from uuid import UUID

from django.db import models
from ninja import Router

from main.apps.core.schemas import NotFoundErrorSchema
from main.di import injector
from main.apps.core.types import AuthedHttpRequest
from main.apps.providers.models import Provider
from main.apps.providers.schemas import ProviderDetailSchema, ProviderSchema
from main.apps.providers.services.provider_retrieval_service import ProviderRetrievalService


providers_router = Router()


@providers_router.get(
    "/",
    url_name="provider_list",
    response={HTTPStatus.OK: list[ProviderSchema]},
    description="List all providers",
)
def get_provider_list(
    request: AuthedHttpRequest,
) -> models.QuerySet[Provider]:
    provider_retrieval_service = injector.get(ProviderRetrievalService)
    return provider_retrieval_service.get_list()


@providers_router.get(
    "/{provider_id}/",
    url_name="provider_detail",
    response={HTTPStatus.OK: ProviderDetailSchema, HTTPStatus.NOT_FOUND: NotFoundErrorSchema},
    description="Get a provider by ID",
)
def get_provider_detail(
    request: AuthedHttpRequest,
    provider_id: UUID,
) -> ProviderDetailSchema:
    provider_retrieval_service = injector.get(ProviderRetrievalService)
    return provider_retrieval_service.get_detail_by_id(provider_id)
