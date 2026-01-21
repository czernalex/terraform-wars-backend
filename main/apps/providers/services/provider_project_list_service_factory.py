from abc import ABC, abstractmethod
from typing import override

from injector import inject

from main.apps.providers.models.provider import Provider
from main.apps.providers.services.provider_project_list_service import ProviderProjectListService
from main.apps.providers.services.gcp_project_list_service import GCPProjectListService


class ProviderProjectListServiceFactory(ABC):
    @abstractmethod
    def get_service(self, provider: Provider) -> ProviderProjectListService:
        pass


class DefaultProviderProjectListServiceFactory(ProviderProjectListServiceFactory):
    @inject
    def __init__(self, gcp_project_list_service: GCPProjectListService):
        self._services_map = {
            gcp_project_list_service.get_provider_id(): gcp_project_list_service,
        }

    @override
    def get_service(self, provider: Provider) -> ProviderProjectListService:
        try:
            return self._services_map[provider.provider_id]
        except KeyError:
            raise NotImplementedError(f"No project list service found for provider: {provider.provider_id}")
