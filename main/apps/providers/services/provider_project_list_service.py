from abc import ABC, abstractmethod
from uuid import UUID

from main.apps.providers.schemas import ProviderProjectSchema


class ProviderProjectListService(ABC):
    @abstractmethod
    def get_list(self, user_id: UUID) -> list[ProviderProjectSchema]:
        pass
