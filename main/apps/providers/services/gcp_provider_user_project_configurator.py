import logging
from typing import override

from django.conf import settings
from django.db import transaction
from injector import inject

from main.apps.gcp.services import (
    GCPImpersonatedCredentialsCreateService,
    GCPProjectIamRoleGrantService,
    GCPServiceAccountImpersonationService,
    GCPServiceEnableService,
)
from main.apps.providers.models import ProviderUserProject
from main.apps.providers.services.provider_user_project_configurator import ProviderUserProjectConfigurator


logger = logging.getLogger(__name__)


class GCPProviderUserProjectConfigurator(ProviderUserProjectConfigurator):
    PROVIDER_ID = "google"

    DEFAULT_PROJECT_APIS = [
        "cloudresourcemanager.googleapis.com",
        "serviceusage.googleapis.com",
        "iam.googleapis.com",
        "iamcredentials.googleapis.com",
        "sts.googleapis.com",
    ]

    @inject
    def __init__(
        self,
        gcp_impersonated_credentials_create_service: GCPImpersonatedCredentialsCreateService,
        gcp_service_enable_service: GCPServiceEnableService,
        gcp_service_account_impersonation_service: GCPServiceAccountImpersonationService,
        gcp_project_iam_role_grant_service: GCPProjectIamRoleGrantService,
    ):
        self._gcp_impersonated_credentials_create_service = gcp_impersonated_credentials_create_service
        self._gcp_service_enable_service = gcp_service_enable_service
        self._gcp_service_account_impersonation_service = gcp_service_account_impersonation_service
        self._gcp_project_iam_role_grant_service = gcp_project_iam_role_grant_service

    def _get_default_project_apis(self) -> list[str]:
        return self.DEFAULT_PROJECT_APIS

    @override
    def get_provider_id(self) -> str:
        return self.PROVIDER_ID

    def _handle_error(self, provider_user_project: ProviderUserProject, error: Exception) -> None:
        # Failing silently is ok here, because cloud scheduler will run this job again
        logger.warning(
            "Error occured while configuring GCP project for provider user project: %(provider_user_project_id)s. Error: %(error)s",
            {
                "provider_user_project_id": provider_user_project.id,
                "error": str(error),
            },
            exc_info=True,
        )

    @override
    @transaction.atomic
    def configure(self, provider_user_project: ProviderUserProject) -> ProviderUserProject:
        logger.info(
            "Configuring GCP project for provider user project: %(provider_user_project_id)s",
            {
                "provider_user_project_id": provider_user_project.id,
            },
        )

        try:
            credentials = self._gcp_impersonated_credentials_create_service.create(
                provider_user_project.config_data["gcp_service_account_email"]
            )
            self._gcp_service_enable_service.enable(
                credentials,
                provider_user_project.config_data["gcp_project_name"],
                self._get_default_project_apis(),
            )
            self._gcp_service_account_impersonation_service.grant_impersonation(
                credentials,
                provider_user_project.config_data["gcp_project_id"],
                provider_user_project.config_data["gcp_service_account_email"],
                [
                    settings.GCP_TERRAFORM_EXECUTOR_SERVICE_ACCOUNT_EMAIL,
                    settings.GCP_TERRAFORM_VALIDATOR_SERVICE_ACCOUNT_EMAIL,
                ],
            )
            self._gcp_project_iam_role_grant_service.grant_role_to_service_account(
                credentials,
                provider_user_project.config_data["gcp_project_id"],
                provider_user_project.config_data["gcp_service_account_email"],
                "roles/serviceusage.serviceUsageAdmin",
            )
        except Exception as error:
            return self._handle_error(provider_user_project, error)

        logger.info(
            "GCP project configured successfully for provider user project: %(provider_user_project_id)s",
            {
                "provider_user_project_id": provider_user_project.id,
            },
        )
        return provider_user_project
