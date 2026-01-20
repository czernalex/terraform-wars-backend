import logging
from typing import override

from ninja.errors import ValidationError

from main.apps.providers.models import Provider
from main.apps.providers.schemas import CreateProviderUserProjectSchema, GCPProviderUserProjectConfigDataSchema
from main.apps.providers.services.provider_user_project_config_data_validation_service import (
    ProviderUserProjectConfigDataValidationService,
)


logger = logging.getLogger(__name__)


class GCPProviderUserProjectConfigDataValidationService(ProviderUserProjectConfigDataValidationService):
    @override
    def validate(self, provider: Provider, data: CreateProviderUserProjectSchema) -> None:
        if not isinstance(data.config_data, GCPProviderUserProjectConfigDataSchema):
            logger.error(
                "Invalid config data %(config_data)s for GCP provider: %(provider_id)s and user %(user_id)s",
                {"config_data": data.config_data, "provider_id": provider.id, "user_id": data.user_id},
            )
            raise ValidationError(
                [
                    {
                        "loc": ["config_data"],
                        "msg": "Invalid config data",
                        "type": "value_error",
                    }
                ]
            )
