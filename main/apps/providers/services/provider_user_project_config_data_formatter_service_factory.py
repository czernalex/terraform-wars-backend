from abc import ABC, abstractmethod
from typing import override

from injector import inject

from main.apps.providers.models import Provider
from main.apps.providers.services.gcp_provider_user_project_config_data_formatter_service import (
    GCPProviderUserProjectConfigDataFormatterService,
)
from main.apps.providers.services.provider_user_project_config_data_formatter_service import (
    ProviderUserProjectConfigDataFormatterService,
)


class ProviderUserProjectConfigDataFormatterServiceFactory(ABC):
    @abstractmethod
    def get_formatter_service(self, provider: Provider) -> ProviderUserProjectConfigDataFormatterService:
        pass


class DefaultProviderUserProjectConfigDataFormatterServiceFactory(ProviderUserProjectConfigDataFormatterServiceFactory):
    @inject
    def __init__(self, gcp_provider_user_project_validation_service: GCPProviderUserProjectConfigDataFormatterService):
        self._formatter_services_map = {
            "google": gcp_provider_user_project_validation_service,
        }

    @override
    def get_formatter_service(self, provider: Provider) -> ProviderUserProjectConfigDataFormatterService:
        try:
            return self._formatter_services_map[provider.provider_id]
        except KeyError:
            raise NotImplementedError(f"No config data formatter service found for provider: {provider.provider_id}")
