from dataclasses import dataclass
from uuid import UUID

from main.apps.providers.models import Provider, ProviderUserProject
from main.apps.tutorials.enums import TutorialStatus
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
