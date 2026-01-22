from django.http import StreamingHttpResponse
from ninja import Router

from main.di import injector
from main.apps.core.types import AuthedHttpRequest
from main.apps.notifications.services import NotificationStreamService


notifications_router = Router()


@notifications_router.get(
    "/",
    url_name="notification_list",
    description="Stream user's notifications over SSE",
)
async def stream_notifications(request: AuthedHttpRequest):
    notification_stream_service = injector.get(NotificationStreamService)
    response = StreamingHttpResponse(
        notification_stream_service.stream(request.user.id),
        content_type="text/event-stream",
    )
    response["Cache-control"] = "no-cache"
    return response
