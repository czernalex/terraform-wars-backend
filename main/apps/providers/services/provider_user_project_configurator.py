from abc import ABC, abstractmethod

from main.apps.providers.models import ProviderUserProject


class ProviderUserProjectConfigurator(ABC):
    @abstractmethod
    def get_provider_id(self) -> str:
        pass

    @abstractmethod
    def configure(self, provider_user_project: ProviderUserProject) -> ProviderUserProject:
        pass
