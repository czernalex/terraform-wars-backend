from http import HTTPStatus

from django.db import models
from ninja import Query, Router
from ninja.pagination import paginate

from main.apps.notifications.services import NotificationRetrievalService, NotificationUpdateService
from main.di import injector
from main.apps.core.types import AuthedHttpRequest
from main.apps.notifications.models import Notification
from main.apps.notifications.schemas import (
    NotificationListFilterSchema,
    NotificationPartialUpdateSchema,
    NotificationSchema,
)


notifications_router = Router()


@notifications_router.get(
    "/",
    url_name="notification_list",
    response={HTTPStatus.OK: list[NotificationSchema]},
    description="List notifications for the authenticated user",
)
@paginate
def get_notification_list(
    request: AuthedHttpRequest, filters: Query[NotificationListFilterSchema]
) -> models.QuerySet[Notification]:
    filters.user_id = request.user.id
    notification_retrieval_service = injector.get(NotificationRetrievalService)
    return notification_retrieval_service.get_list(
        filters,
        ordering=(
            "dispatched",
            "-created_at",
        ),
    )


@notifications_router.patch(
    "/{notification_id}/",
    url_name="notification_detail",
    response={HTTPStatus.OK: NotificationSchema},
    description="Partial update a notification for the authenticated user",
)
def partial_update_notification(
    request: AuthedHttpRequest, notification_id: int, data: NotificationPartialUpdateSchema
) -> Notification:
    notification_update_service = injector.get(NotificationUpdateService)
    return notification_update_service.partial_update(request.user.id, notification_id, data)
