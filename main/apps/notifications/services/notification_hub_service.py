import logging
from asyncio import Queue
from uuid import UUID


logger = logging.getLogger(__name__)


class NotificationHubService:
    def __init__(self):
        self._user_queues: dict[UUID, set[Queue[int]]] = dict()

    def add_subscriber(self, user_id: UUID) -> Queue:
        queue = Queue[int]()
        if user_id not in self._user_queues:
            self._user_queues[user_id] = set[Queue[int]]()
        self._user_queues[user_id].add(queue)
        logger.info(f"Added subscriber: {user_id}")
        return queue

    def remove_subscriber(self, user_id: UUID, queue: Queue) -> None:
        if user_id not in self._user_queues:
            return
        self._user_queues[user_id].remove(queue)
        if not self._user_queues[user_id]:
            del self._user_queues[user_id]
        logger.info(f"Removed subscriber: {user_id}")

    async def abroadcast(self, user_id: UUID, notification_id: int) -> None:
        if user_id not in self._user_queues:
            return
        for queue in self._user_queues[user_id]:
            await queue.put(notification_id)
        logger.info(f"Broadcasted notification: {notification_id} to subscribers: {user_id}")
