import logging


from main.apps.notifications.models import Notification


logger = logging.getLogger(__name__)


class NotificationUpdateService:
    async def mark_as_dispatched(self, notification: Notification) -> None:
        logger.info(f"Marking notification as dispatched: {notification.id}")
        notification.dispatched = True
        await notification.asave()
        logger.info(f"Notification: {notification.id} marked as dispatched")
