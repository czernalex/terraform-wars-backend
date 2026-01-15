from abc import ABC, abstractmethod
from typing import override

from injector import inject

from main.apps.tutorials.models import TutorialProject
from main.apps.tutorials.services.gcp_tutorial_project_resources_destroy_service import (
    GCPTutorialProjectResourcesDestroyService,
)
from main.apps.tutorials.services.tutorial_project_resources_destroy_service import (
    TutorialProjectResourcesDestroyService,
)


class TutorialProjectResourcesDestroyServiceFactory(ABC):
    @abstractmethod
    def get_service(self, tutorial_project: TutorialProject) -> TutorialProjectResourcesDestroyService:
        pass


class DefaultTutorialProjectResourcesDestroyServiceFactory(TutorialProjectResourcesDestroyServiceFactory):
    @inject
    def __init__(self, gcp_tutorial_project_resources_destroy_service: GCPTutorialProjectResourcesDestroyService):
        self._services_map = {
            gcp_tutorial_project_resources_destroy_service.get_provider_id(): gcp_tutorial_project_resources_destroy_service,
        }

    @override
    def get_service(self, tutorial_project: TutorialProject) -> TutorialProjectResourcesDestroyService:
        try:
            return self._services_map[tutorial_project.tutorial.provider.provider_id]
        except KeyError:
            raise NotImplementedError(
                f"No service found for provider: {tutorial_project.tutorial.provider.provider_id}"
            )
