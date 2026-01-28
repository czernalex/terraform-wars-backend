from abc import ABC, abstractmethod

from google.cloud import run_v2

from main.apps.tutorials.models.tutorial_submission import TutorialSubmission


class ExecutorEnvironmentConfigurator(ABC):
    """
    For each provider, we need to configure different environment variables for the cloud run job, that is responsible
    for executing the submitted terraform code. Therefore, each supported provider needs to implement this interface.
    """

    @abstractmethod
    def configure(self, tutorial_submission: TutorialSubmission) -> list[run_v2.EnvVar]:
        pass
