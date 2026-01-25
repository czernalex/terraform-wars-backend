import msgspec
from uuid import UUID


class NotificationMessage(msgspec.Struct):
    user_id: UUID
    notification_id: int
