import logging
from asyncio import Queue
from uuid import UUID


logger = logging.getLogger(__name__)


class TutorialSubmissionEventHubService:
    def __init__(self):
        self._user_submission_queues: dict[(UUID, UUID), set[Queue[UUID]]] = dict()

    def add_subscriber(self, user_id: UUID, tutorial_submission_id: UUID) -> Queue[UUID]:
        queue = Queue[UUID]()
        if (user_id, tutorial_submission_id) not in self._user_submission_queues:
            self._user_submission_queues[(user_id, tutorial_submission_id)] = set[Queue[UUID]]()
        self._user_submission_queues[(user_id, tutorial_submission_id)].add(queue)
        logger.info(f"Added subscriber: {user_id} for tutorial submission: {tutorial_submission_id}")
        return queue

    def remove_subscriber(self, user_id: UUID, tutorial_submission_id: UUID, queue: Queue[UUID]) -> None:
        if (user_id, tutorial_submission_id) not in self._user_submission_queues:
            return
        self._user_submission_queues[(user_id, tutorial_submission_id)].remove(queue)
        if not self._user_submission_queues[(user_id, tutorial_submission_id)]:
            del self._user_submission_queues[(user_id, tutorial_submission_id)]
        logger.info(f"Removed subscriber: {user_id} for tutorial submission: {tutorial_submission_id}")

    async def abroadcast(self, user_id: UUID, tutorial_submission_id: UUID, tutorial_submission_event_id: UUID) -> None:
        if (user_id, tutorial_submission_id) not in self._user_submission_queues:
            return
        for queue in self._user_submission_queues[(user_id, tutorial_submission_id)]:
            await queue.put(tutorial_submission_event_id)
        logger.info(
            f"Broadcasted tutorial submission event: {tutorial_submission_event_id} to subscribers: {user_id} for tutorial submission: {tutorial_submission_id}"
        )
