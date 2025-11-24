from http import HTTPStatus

from anydi import auto
from django.db import models
from ninja import Router

from main.apps.core.types import AuthedHttpRequest
from main.apps.tutorials.models import Provider
from main.apps.tutorials.schemas import ProviderSchema
from main.apps.tutorials.services.provider_retrieval_service import ProviderRetrievalService


providers_router = Router()


@providers_router.get(
    "/",
    url_name="provider_list",
    response={HTTPStatus.OK: list[ProviderSchema]},
    description="List all providers",
)
def get_provider_list(
    request: AuthedHttpRequest, provider_retrieval_service: ProviderRetrievalService = auto
) -> models.QuerySet[Provider]:
    return provider_retrieval_service.get_provider_list()
