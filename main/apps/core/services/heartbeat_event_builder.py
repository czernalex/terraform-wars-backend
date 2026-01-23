from django.utils import timezone


class HeartbeatEventBuilder:
    def build_event(self) -> str:
        return f"event: heartbeat\ndata: {timezone.now().isoformat()}\n\n"
