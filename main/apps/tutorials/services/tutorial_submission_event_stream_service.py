import asyncio
import logging
from typing import AsyncIterator
from uuid import UUID

from injector import inject

from main.apps.core.services import HeartbeatEventBuilder
from main.apps.tutorials.schemas import TutorialSubmissionEventEventSchema
from main.apps.tutorials.services.tutorial_submission_event_event_builder import TutorialSubmissionEventEventBuilder
from main.apps.tutorials.services.tutorial_submission_event_hub_service import TutorialSubmissionEventHubService
from main.apps.tutorials.services.tutorial_submission_event_retrieval_service import (
    TutorialSubmissionEventRetrievalService,
)


logger = logging.getLogger(__name__)


class TutorialSubmissionEventStreamService:
    @inject
    def __init__(
        self,
        heartbeat_event_builder: HeartbeatEventBuilder,
        tutorial_submission_event_hub_service: TutorialSubmissionEventHubService,
        tutorial_submission_event_retrieval_service: TutorialSubmissionEventRetrievalService,
        tutorial_submission_event_event_builder: TutorialSubmissionEventEventBuilder,
    ):
        self._heartbeat_event_builder = heartbeat_event_builder
        self._tutorial_submission_event_hub_service = tutorial_submission_event_hub_service
        self._tutorial_submission_event_retrieval_service = tutorial_submission_event_retrieval_service
        self._tutorial_submission_event_event_builder = tutorial_submission_event_event_builder

    async def astream(self, user_id: UUID, tutorial_submission_id: UUID) -> AsyncIterator[str]:
        queue = self._tutorial_submission_event_hub_service.add_subscriber(user_id, tutorial_submission_id)
        yield self._heartbeat_event_builder.build_event()  # Send initial heartbeat event
        try:
            while True:
                try:
                    tutorial_submission_event_id = await asyncio.wait_for(queue.get(), timeout=30.0)
                    tutorial_submission_event = (
                        await self._tutorial_submission_event_retrieval_service.aget_for_read_by_id(
                            user_id,
                            tutorial_submission_event_id,
                        )
                    )
                    logger.info(
                        f"Tutorial submission event: {tutorial_submission_event.id} sent to the user: {user_id}"
                    )
                    tutorial_submission_event_event = TutorialSubmissionEventEventSchema(
                        id=tutorial_submission_event.id,
                        tutorial_submission_id=tutorial_submission_event.tutorial_submission_id,
                        event_status=tutorial_submission_event.event_status,
                        exit_code=tutorial_submission_event.exit_code,
                        stdout=tutorial_submission_event.stdout,
                        error=tutorial_submission_event.error,
                    )
                    yield self._tutorial_submission_event_event_builder.build_event(tutorial_submission_event_event)
                except asyncio.TimeoutError:
                    logger.info(
                        f"No new tutorial submission events received within the timeout. Sending heartbeat event to the user: {user_id}"
                    )
                    yield self._heartbeat_event_builder.build_event()
        finally:
            self._tutorial_submission_event_hub_service.remove_subscriber(user_id, queue)
