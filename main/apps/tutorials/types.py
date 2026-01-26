from dataclasses import dataclass
from uuid import UUID

from main.apps.providers.models import Provider
from main.apps.tutorials.enums import TutorialStatus


@dataclass(frozen=True)
class CreateTutorialValidatedData:
    provider: Provider
    slug: str
    status: TutorialStatus
    tag_ids: list[UUID]
