import logging
from typing import override

from main.apps.providers.models import Provider
from main.apps.providers.schemas import CreateProviderUserProjectSchema
from main.apps.providers.services.provider_user_project_config_data_formatter_service import (
    ProviderUserProjectConfigDataFormatterService,
)


logger = logging.getLogger(__name__)


class GCPProviderUserProjectConfigDataFormatterService(ProviderUserProjectConfigDataFormatterService):
    @override
    def format(self, provider: Provider, data: CreateProviderUserProjectSchema) -> dict[str, str]:
        return {
            "gcp_project_id": data.project_id,
            "gcp_project_name": data.project_number,
            "gcp_service_account_email": f"terraform-wars-sa@{data.project_id}.iam.gserviceaccount.com",
        }
