from abc import ABC, abstractmethod
from typing import override

from injector import inject

from main.apps.tasks.services.executor_environment_configurator import ExecutorEnvironmentConfigurator
from main.apps.tutorials.models.tutorial_submission import TutorialSubmission
from main.apps.tasks.services.google_provider_executor_environment_configurator import (
    GoogleProviderExecutorEnvironmentConfigurator,
)


class ExecutorEnvironmentConfiguratorFactory(ABC):
    @abstractmethod
    def get_configurator(self, tutorial_submission: TutorialSubmission) -> ExecutorEnvironmentConfigurator:
        pass


class DefaultExecutorEnvironmentConfiguratorFactory(ExecutorEnvironmentConfiguratorFactory):
    @inject
    def __init__(
        self, google_provider_executor_environment_configurator: GoogleProviderExecutorEnvironmentConfigurator
    ):
        self._configurators_map = {
            "google": google_provider_executor_environment_configurator,
        }

    @override
    def get_configurator(self, tutorial_submission: TutorialSubmission) -> ExecutorEnvironmentConfigurator:
        try:
            return self._configurators_map[tutorial_submission.provider_id]
        except KeyError:
            raise NotImplementedError(f"No configurator found for provider: {tutorial_submission.provider_id}")
