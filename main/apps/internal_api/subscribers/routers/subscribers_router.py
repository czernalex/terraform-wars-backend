from http import HTTPStatus

from django.http import HttpRequest
from ninja import Router

from main.apps.internal_api.subscribers.schemas import PubSubEnvelopeSchema
from main.di import injector
from main.apps.internal_api.subscribers.services import (
    TutorialSubmissionExecutionFinishedHandler,
    TutorialSubmissionValidationFinishedHandler,
)


subscribers_router = Router()


@subscribers_router.post(
    "/submissions/execute/",
    url_name="submission_execution_finished",
    response={HTTPStatus.NO_CONTENT: None},
    description="Subscribe to a submission execution finished event",
)
def subscribe_to_submission_execution_finished(request: HttpRequest, data: PubSubEnvelopeSchema) -> None:
    tutorial_submission_execution_finished_handler = injector.get(TutorialSubmissionExecutionFinishedHandler)
    tutorial_submission_execution_finished_handler.handle(data)


@subscribers_router.post(
    "/submissions/validate/",
    url_name="subscribe_to_submission_validation_finished",
    response={HTTPStatus.NO_CONTENT: None},
    description="Subscribe to a submission validation finished event",
)
def subscribe_to_submission_validation_finished(request: HttpRequest, data: PubSubEnvelopeSchema) -> None:
    tutorial_submission_validation_finished_handler = injector.get(TutorialSubmissionValidationFinishedHandler)
    tutorial_submission_validation_finished_handler.handle(data)
