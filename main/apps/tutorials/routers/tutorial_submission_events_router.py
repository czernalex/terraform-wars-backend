from http import HTTPStatus
from uuid import UUID

from django.http import StreamingHttpResponse
from ninja import Router

from main.apps.tutorials.services import TutorialSubmissionEventStreamService
from main.di import injector
from main.apps.core.types import AuthedHttpRequest


tutorial_submission_events_router = Router()


@tutorial_submission_events_router.get(
    "/{tutorial_submission_id}/events/",
    url_name="tutorial_submission_detail_events_list",
    response={HTTPStatus.BAD_REQUEST: None},
    openapi_extra={
        "responses": {
            "200": {
                "description": "Server-Sent Events stream",
                "content": {
                    "text/event-stream": {
                        "schema": {
                            "type": "string",
                            "example": (
                                'event: message\nid: 123\ndata: {"id":123,"tutorial_submission_id":123,"event_status":"pending","exit_code":0,"stdout":"Hello","error":"Error"}\n\n'
                            ),
                        }
                    }
                },
            }
        }
    },
)
async def astream_tutorial_submission_events(
    request: AuthedHttpRequest, tutorial_submission_id: UUID
) -> StreamingHttpResponse:
    tutorial_submission_event_stream_service = injector.get(TutorialSubmissionEventStreamService)
    response = StreamingHttpResponse(
        tutorial_submission_event_stream_service.astream(request.user.id, tutorial_submission_id),
        content_type="text/event-stream",
    )
    response["Cache-control"] = "no-cache"
    response["Connection"] = "keep-alive"
    response["X-Accel-Buffering"] = "no"
    return response
