from abc import ABC, abstractmethod

from main.apps.providers.models import Provider
from main.apps.providers.schemas import CreateProviderUserProjectSchema


class ProviderUserProjectConfigDataFormatterService(ABC):
    @abstractmethod
    def format(self, provider: Provider, data: CreateProviderUserProjectSchema) -> dict[str, str]:
        pass
