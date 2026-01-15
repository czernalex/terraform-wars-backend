from http import HTTPStatus

from django.db import models
from ninja import Router

from main.di import injector
from main.apps.core.types import AuthedHttpRequest
from main.apps.tutorials.schemas import TutorialTagSchema
from main.apps.tutorials.services import TutorialTagRetrievalService
from main.apps.tutorials.models import TutorialTag


tutorial_tags_router = Router()


@tutorial_tags_router.get(
    "/",
    url_name="tutorial_tag_list",
    response={HTTPStatus.OK: list[TutorialTagSchema]},
    description="List all tutorial tags",
)
def get_tutorial_tag_list(
    request: AuthedHttpRequest,
) -> models.QuerySet[TutorialTag]:
    tutorial_tag_retrieval_service = injector.get(TutorialTagRetrievalService)
    return tutorial_tag_retrieval_service.get_list()
