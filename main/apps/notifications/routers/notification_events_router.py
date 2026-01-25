from http import HTTPStatus

from django.http import StreamingHttpResponse
from ninja import Router

from main.di import injector
from main.apps.core.types import AuthedHttpRequest
from main.apps.notifications.services import NotificationStreamService


notification_events_router = Router()


# Somehow django ninja does not support editing default response schema using
# openapi_extra. This is a workaround to provide example schema in openapi documentation.
@notification_events_router.get(
    "/",
    url_name="notification_event_list",
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
                                'event: notification\nid: 123\ndata: {"id":123,"text":"Hello","level":"info"}\n\n'
                            ),
                        }
                    }
                },
            }
        }
    },
)
async def astream_notifications(request: AuthedHttpRequest) -> StreamingHttpResponse:
    notification_stream_service = injector.get(NotificationStreamService)
    response = StreamingHttpResponse(
        notification_stream_service.astream(request.user.id),
        content_type="text/event-stream",
    )
    response["Cache-control"] = "no-cache"
    response["Connection"] = "keep-alive"
    response["X-Accel-Buffering"] = "no"
    return response
