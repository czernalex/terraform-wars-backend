from uuid import UUID

from main.apps.users.models import User
from main.apps.tutorials.models import TutorialProject


class TutorialProjectRetrievalService:
    def get_tutorial_project_detail(self, user: User, tutorial_project_id: UUID) -> TutorialProject:
        pass
