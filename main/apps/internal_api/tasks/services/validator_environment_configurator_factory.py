from abc import ABC, abstractmethod
from typing import override

from injector import inject

from main.apps.internal_api.tasks.services.validator_environment_configurator import ValidatorEnvironmentConfigurator
from main.apps.tutorials.models.tutorial_submission import TutorialSubmission
from main.apps.internal_api.tasks.services.google_provider_validator_environment_configurator import (
    GoogleProviderValidatorEnvironmentConfigurator,
)


class ValidatorEnvironmentConfiguratorFactory(ABC):
    @abstractmethod
    def get_configurator(self, tutorial_submission: TutorialSubmission) -> ValidatorEnvironmentConfigurator:
        pass


class DefaultValidatorEnvironmentConfiguratorFactory(ValidatorEnvironmentConfiguratorFactory):
    @inject
    def __init__(
        self, google_provider_validator_environment_configurator: GoogleProviderValidatorEnvironmentConfigurator
    ):
        self._configurators_map = {
            "google": google_provider_validator_environment_configurator,
        }

    @override
    def get_configurator(self, tutorial_submission: TutorialSubmission) -> ValidatorEnvironmentConfigurator:
        try:
            return self._configurators_map[tutorial_submission.provider_id]
        except KeyError:
            raise NotImplementedError(f"No configurator found for provider: {tutorial_submission.provider_id}")
