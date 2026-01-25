from typing import Optional, Annotated
from datetime import datetime
from uuid import UUID

from ninja import FilterLookup, FilterSchema, ModelSchema, Schema

from main.apps.notifications.enums import NotificationLevel
from main.apps.notifications.models import Notification


class NotificationListFilterSchema(FilterSchema):
    user_id: Optional[UUID] = None
    dispatched: Optional[bool] = None
    read: Optional[bool] = None
    last_event_id: Annotated[Optional[int], FilterLookup("id__gt")] = None
    created_at: Annotated[Optional[datetime], FilterLookup("created_at__gte")] = None


class NotificationEventSchema(Schema):
    id: int
    text: str
    level: NotificationLevel


class NotificationCreateSchema(Schema):
    text: str
    level: NotificationLevel


class NotificationPartialUpdateSchema(Schema):
    dispatched: Optional[bool] = None
    read: Optional[bool] = None


class NotificationSchema(ModelSchema):
    id: int
    user_id: UUID
    level: NotificationLevel

    class Meta:
        model = Notification
        fields = [
            "text",
            "dispatched",
            "read",
            "created_at",
        ]
