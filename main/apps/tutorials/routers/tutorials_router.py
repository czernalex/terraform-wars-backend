from http import HTTPStatus

from anydi import auto
from django.db import models
from ninja import Router
from ninja.pagination import paginate

from main.apps.core.types import AuthedHttpRequest
from main.apps.tutorials.models import Tutorial
from main.apps.tutorials.schemas import TutorialListSchema
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
    request: AuthedHttpRequest, tutorial_retrieval_service: TutorialRetrievalService = auto
) -> models.QuerySet[Tutorial]:
    return tutorial_retrieval_service.get_tutorial_list()
