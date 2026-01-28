from uuid import UUID
from typing import Optional

import msgspec


class TutorialSubmissionExecutionFinishedMessage(msgspec.Struct):
    user_id: UUID
    tutorial_submission_id: UUID
    exit_code: int
    stdout: Optional[str] = None
    stderr: Optional[str] = None


class TutorialSubmissionValidationFinishedMessage(msgspec.Struct):
    user_id: UUID
    tutorial_submission_id: UUID
    exit_code: int
    stdout: Optional[str] = None
    stderr: Optional[str] = None
