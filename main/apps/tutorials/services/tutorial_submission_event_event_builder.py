from typing import AsyncIterable
from uuid import UUID

import msgspec

from main.apps.tutorials.models import TutorialSubmissionEvent
from main.apps.tutorials.types import TutorialSubmissionEventSchemaMessage


class TutorialSubmissionEventEventBuilder:
    async def build_event(
        self,
        tutorial_submission_event_id: UUID,
        tutorial_submission_event_events: AsyncIterable[TutorialSubmissionEvent],
    ) -> str:
        data = [
            TutorialSubmissionEventSchemaMessage(
                id=tutorial_submission_event.id,
                tutorial_submission_id=tutorial_submission_event.tutorial_submission_id,
                event_status=tutorial_submission_event.event_status,
                exit_code=tutorial_submission_event.exit_code,
                stdout=tutorial_submission_event.stdout,
                error=tutorial_submission_event.error,
            )
            async for tutorial_submission_event in tutorial_submission_event_events
        ]
        return (
            f"event: message\nid: {tutorial_submission_event_id}\ndata: {msgspec.json.encode(data).decode('utf-8')}\n\n"
        )
