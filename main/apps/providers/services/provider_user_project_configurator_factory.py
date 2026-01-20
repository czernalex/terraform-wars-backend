import logging
from abc import ABC, abstractmethod
from typing import override

from injector import inject

from main.apps.providers.models import ProviderUserProject
from main.apps.providers.services.gcp_provider_user_project_configurator import GCPProviderUserProjectConfigurator
from main.apps.providers.services.provider_user_project_configurator import ProviderUserProjectConfigurator


logger = logging.getLogger(__name__)


class ProviderUserProjectConfiguratorFactory(ABC):
    @abstractmethod
    def get_configurator(self, provider_user_project: ProviderUserProject) -> ProviderUserProjectConfigurator:
        pass


class DefaultProviderUserProjectConfiguratorFactory(ProviderUserProjectConfiguratorFactory):
    @inject
    def __init__(self, gcp_provider_user_project_configurator: GCPProviderUserProjectConfigurator):
        self._configurators_map = {
            gcp_provider_user_project_configurator.get_provider_id(): gcp_provider_user_project_configurator,
        }

    @override
    def get_configurator(self, provider_user_project: ProviderUserProject) -> ProviderUserProjectConfigurator:
        try:
            return self._configurators_map[provider_user_project.provider.provider_id]
        except KeyError:
            logger.error(f"No configurator found for provider: {provider_user_project.provider.provider_id}")
            raise NotImplementedError(
                f"No configurator found for provider: {provider_user_project.provider.provider_id}"
            )
