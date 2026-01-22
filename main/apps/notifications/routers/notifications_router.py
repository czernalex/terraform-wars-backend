from http import HTTPStatus

from django.http import StreamingHttpResponse
from ninja import Router

from main.di import injector
from main.apps.core.types import AuthedHttpRequest
from main.apps.notifications.services import NotificationStreamService


notifications_router = Router()


@notifications_router.get(
    "/",
    url_name="notification_list",
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
async def stream_notifications(request: AuthedHttpRequest) -> StreamingHttpResponse:
    last_event_id = request.headers.get("Last-Event-ID")
    notification_stream_service = injector.get(NotificationStreamService)
    response = StreamingHttpResponse(
        notification_stream_service.stream(request.user.id, last_event_id),
        content_type="text/event-stream",
    )
    response["Cache-control"] = "no-cache"
    return response
