from injector import inject
from main.apps.tutorials.schemas import CreateTutorialStepSubmissionSchema
from main.apps.tutorials.services.tutorial_retrieval_service import TutorialRetrievalService
from main.apps.tutorials.services.tutorial_step_retrieval_service import TutorialStepRetrievalService
from main.apps.users.models import User


class TutorialStepSubmissionService:
    @inject
    def __init__(
        self,
        tutorial_retrieval_service: TutorialRetrievalService,
        tutorial_step_retrieval_service: TutorialStepRetrievalService,
    ) -> None:
        self.tutorial_retrieval_service = tutorial_retrieval_service
        self.tutorial_step_retrieval_service = tutorial_step_retrieval_service

    def create_tutorial_step_submission(self, user: User, data: CreateTutorialStepSubmissionSchema) -> None:
        pass
