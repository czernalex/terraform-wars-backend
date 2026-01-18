from abc import ABC, abstractmethod

from google.cloud import run_v2

from main.apps.tutorials.models.tutorial_submission import TutorialSubmission


class ValidatorEnvironmentConfigurator(ABC):
    @abstractmethod
    def configure(self, tutorial_submission: TutorialSubmission) -> list[run_v2.EnvVar]:
        pass
