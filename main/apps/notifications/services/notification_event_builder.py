from main.apps.notifications.schemas import NotificationEventSchema


class NotificationEventBuilder:
    def build_event(self, notification_event: NotificationEventSchema) -> str:
        return f"event: message\nid: {notification_event.id}\ndata: {notification_event.model_dump_json()}\n\n"
