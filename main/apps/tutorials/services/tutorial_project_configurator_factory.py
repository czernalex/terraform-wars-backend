from abc import ABC, abstractmethod
from typing import override

from injector import inject

from main.apps.tutorials.models import TutorialProject
from main.apps.tutorials.services.tutorial_project_configurator import (
    TutorialProjectConfigurator,
    GCPTutorialProjectConfigurator,
)


class TutorialProjectConfiguratorFactory(ABC):
    @abstractmethod
    def get_configurator(self, tutorial_project: TutorialProject) -> TutorialProjectConfigurator:
        pass


class DefaultTutorialProjectConfiguratorFactory(TutorialProjectConfiguratorFactory):
    @inject
    def __init__(self, gcp_tutorial_project_configurator: GCPTutorialProjectConfigurator):
        self._configurators_map = {
            gcp_tutorial_project_configurator.get_provider_id(): gcp_tutorial_project_configurator,
        }

    @override
    def get_configurator(self, tutorial_project: TutorialProject) -> TutorialProjectConfigurator:
        try:
            return self._configurators_map[tutorial_project.tutorial.provider.provider_id]
        except KeyError:
            raise NotImplementedError(
                f"No configurator found for provider: {tutorial_project.tutorial.provider.provider_id}"
            )
