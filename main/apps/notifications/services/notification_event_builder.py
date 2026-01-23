from main.apps.notifications.models import Notification
from main.apps.notifications.schemas import NotificationEventSchema


class NotificationEventBuilder:
    def build_event(self, notification: Notification) -> str:
        event = NotificationEventSchema(
            id=notification.id,
            text=notification.text,
            level=notification.level,
        )
        return f"event: message\nid: {notification.id}\ndata: {event.model_dump_json()}\n\n"
