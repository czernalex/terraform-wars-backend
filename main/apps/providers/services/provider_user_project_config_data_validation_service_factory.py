from abc import ABC, abstractmethod
from typing import override

from injector import inject

from main.apps.providers.models import Provider
from main.apps.providers.services.gcp_provider_user_project_config_data_validation_service import (
    GCPProviderUserProjectConfigDataValidationService,
)
from main.apps.providers.services.provider_user_project_config_data_validation_service import (
    ProviderUserProjectConfigDataValidationService,
)


class ProviderUserProjectConfigDataValidationServiceFactory(ABC):
    @abstractmethod
    def get_validation_service(self, provider: Provider) -> ProviderUserProjectConfigDataValidationService:
        pass


class DefaultProviderUserProjectConfigDataValidationServiceFactory(
    ProviderUserProjectConfigDataValidationServiceFactory
):
    @inject
    def __init__(self, gcp_provider_user_project_validation_service: GCPProviderUserProjectConfigDataValidationService):
        self._validation_services_map = {
            "google": gcp_provider_user_project_validation_service,
        }

    @override
    def get_validation_service(self, provider: Provider) -> ProviderUserProjectConfigDataValidationService:
        try:
            return self._validation_services_map[provider.provider_id]
        except KeyError:
            raise NotImplementedError(f"No config data validation service found for provider: {provider.provider_id}")
