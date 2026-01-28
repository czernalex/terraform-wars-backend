from http import HTTPStatus

from django.db import models
from ninja import Query, Router

from main.apps.tutorials.services import TutorialReviewRetrievalService
from main.di import injector
from main.apps.core.types import AuthedHttpRequest
from main.apps.tutorials.schemas import TutorialReviewListFilterSchema, TutorialReviewSchema
from main.apps.tutorials.models import TutorialReview


tutorial_reviews_router = Router()


@tutorial_reviews_router.get(
    "/",
    url_name="tutorial_review_list",
    response={HTTPStatus.OK: list[TutorialReviewSchema]},
    description="Create a new tutorial review for the authenticated user and the selected tutorial.",
)
def get_tutorial_review_list(
    request: AuthedHttpRequest, filters: Query[TutorialReviewListFilterSchema]
) -> models.QuerySet[TutorialReview]:
    filters.user_id = request.user.id
    tutorial_review_retrieval_service = injector.get(TutorialReviewRetrievalService)
    return tutorial_review_retrieval_service.get_list(filters)
