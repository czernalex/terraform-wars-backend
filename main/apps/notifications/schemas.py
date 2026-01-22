from typing import Optional, Annotated
from datetime import datetime
from uuid import UUID

from ninja import FilterLookup, FilterSchema, Schema

from main.apps.notifications.enums import NotificationLevel


class NotificationListFilterSchema(FilterSchema):
    user_id: Optional[UUID] = None
    dispatched: Optional[bool] = None
    created_at: Annotated[Optional[datetime], FilterLookup("created_at__gte")] = None


class NotificationEventSchema(Schema):
    id: int
    text: str
    level: NotificationLevel
