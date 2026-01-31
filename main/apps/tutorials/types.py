from dataclasses import dataclass
from uuid import UUID

import msgspec

from main.apps.providers.models import Provider, ProviderUserProject
from main.apps.tutorials.enums import TutorialStatus, TutorialSubmissionStatus
from main.apps.tutorials.models import Tutorial


@dataclass(frozen=True)
class CreateOrUpdateTutorialValidatedData:
    provider: Provider
    slug: str
    status: TutorialStatus
    tag_ids: list[UUID]


@dataclass(frozen=True)
class CreateTutorialSubmissionValidatedData:
    tutorial: Tutorial
    provider_user_project: ProviderUserProject
    code: str


class TutorialSubmissionEventMessage(msgspec.Struct):
    user_id: UUID
    tutorial_submission_id: UUID
    tutorial_submission_event_id: UUID


class TutorialSubmissionEventSchemaMessage(msgspec.Struct):
    id: UUID
    tutorial_submission_id: UUID
    event_status: TutorialSubmissionStatus
    exit_code: int
    stdout: str
    error: str
