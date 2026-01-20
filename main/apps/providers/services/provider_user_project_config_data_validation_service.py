from abc import ABC, abstractmethod

from main.apps.providers.models import Provider
from main.apps.providers.schemas import CreateProviderUserProjectSchema


class ProviderUserProjectConfigDataValidationService(ABC):
    @abstractmethod
    def validate(self, provider: Provider, data: CreateProviderUserProjectSchema) -> None:
        pass
