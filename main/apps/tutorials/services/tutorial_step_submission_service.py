from anydi import auto, singleton

from main.apps.tutorials.schemas import CreateTutorialStepSubmissionSchema
from main.apps.tutorials.services.tutorial_retrieval_service import TutorialRetrievalService
from main.apps.tutorials.services.tutorial_step_retrieval_service import TutorialStepRetrievalService
from main.apps.users.models import User


@singleton
class TutorialStepSubmissionService:
    def __init__(
        self,
        tutorial_retrieval_service: TutorialRetrievalService = auto,
        tutorial_step_retrieval_service: TutorialStepRetrievalService = auto,
    ) -> None:
        self.tutorial_retrieval_service = tutorial_retrieval_service
        self.tutorial_step_retrieval_service = tutorial_step_retrieval_service

    def create_tutorial_step_submission(self, user: User, data: CreateTutorialStepSubmissionSchema) -> None:
        pass
