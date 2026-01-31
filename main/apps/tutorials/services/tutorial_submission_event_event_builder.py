from typing import AsyncIterable
from uuid import UUID

from main.apps.tutorials.models import TutorialSubmissionEvent
from main.apps.tutorials.schemas import TutorialSubmissionEventSchema


class TutorialSubmissionEventEventBuilder:
    async def build_event(
        self,
        tutorial_submission_event_id: UUID,
        tutorial_submission_event_events: AsyncIterable[TutorialSubmissionEvent],
    ) -> str:
        data = [
            TutorialSubmissionEventSchema.from_orm(tutorial_submission_event).model_dump_json()
            async for tutorial_submission_event in tutorial_submission_event_events
        ]
        return f"event: message\nid: {tutorial_submission_event_id}\ndata: {data}\n\n"
