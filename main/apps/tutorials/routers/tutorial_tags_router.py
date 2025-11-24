from http import HTTPStatus

from anydi import auto
from django.db import models
from ninja import Router

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
    request: AuthedHttpRequest, tutorial_tag_retrieval_service: TutorialTagRetrievalService = auto
) -> models.QuerySet[TutorialTag]:
    return tutorial_tag_retrieval_service.get_tutorial_tag_list()
