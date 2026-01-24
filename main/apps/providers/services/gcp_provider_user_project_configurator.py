import logging
from typing import override

from django.conf import settings
from django.db import transaction
from google.auth.credentials import Credentials
from injector import inject

from main.apps.gcp.services import (
    GCPImpersonatedCredentialsCreateService,
    GCPProjectIamRoleGrantService,
    GCPServiceAccountImpersonationService,
    GCPServiceEnableService,
    GCPProjectBillingInfoGetService,
)
from main.apps.providers.exceptions import ProviderUserProjectConfigurationError
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
        gcp_project_billing_info_get_service: GCPProjectBillingInfoGetService,
    ):
        self._gcp_impersonated_credentials_create_service = gcp_impersonated_credentials_create_service
        self._gcp_service_enable_service = gcp_service_enable_service
        self._gcp_service_account_impersonation_service = gcp_service_account_impersonation_service
        self._gcp_project_iam_role_grant_service = gcp_project_iam_role_grant_service
        self._gcp_project_billing_info_get_service = gcp_project_billing_info_get_service

    def _get_default_project_apis(self) -> list[str]:
        return self.DEFAULT_PROJECT_APIS

    @override
    def get_provider_id(self) -> str:
        return self.PROVIDER_ID

    def _create_credentials(self, provider_user_project: ProviderUserProject) -> Credentials:
        try:
            return self._gcp_impersonated_credentials_create_service.create(
                provider_user_project.config_data["gcp_service_account_email"]
            )
        except Exception as error:
            logger.warning(
                f"Unable to obtain google auth credentials for provider user project: {provider_user_project.id}. Error: {str(error)}"
            )
            error_message = f"""
                We were not able to obtain google auth credentials for the service account {provider_user_project.config_data["gcp_service_account_email"]}.
                Please ensure, that the service account exists and is properly configured."""
            raise ProviderUserProjectConfigurationError(error_message) from error

    def _enable_project_apis(self, credentials: Credentials, provider_user_project: ProviderUserProject) -> None:
        try:
            self._gcp_service_enable_service.enable(
                credentials,
                provider_user_project.config_data["gcp_project_name"],
                self._get_default_project_apis(),
            )
        except Exception as error:
            logger.warning(
                f"Unable to enable project APIs for provider user project: {provider_user_project.id}. Error: {str(error)}"
            )
            error_message = f"""
                We were not able to enable basic GCP project APIs for the project {provider_user_project.config_data["gcp_project_name"]}.
                Please ensure, that the service account {provider_user_project.config_data["gcp_service_account_email"]} has the owner role on the project."""
            raise ProviderUserProjectConfigurationError(error_message) from error

    def _grant_impersonation_to_service_accounts(
        self, credentials: Credentials, provider_user_project: ProviderUserProject
    ) -> None:
        try:
            self._gcp_service_account_impersonation_service.grant_impersonation(
                credentials,
                provider_user_project.config_data["gcp_project_id"],
                provider_user_project.config_data["gcp_service_account_email"],
                [
                    settings.GCP_TERRAFORM_EXECUTOR_SERVICE_ACCOUNT_EMAIL,
                    settings.GCP_TERRAFORM_VALIDATOR_SERVICE_ACCOUNT_EMAIL,
                ],
            )
        except Exception as error:
            logger.warning(
                f"Unable to grant impersonation to executor and validator service accounts for provider user project: {provider_user_project.id}. Error: {str(error)}"
            )
            error_message = f"""
            We were not able to finish the configuration of the project {provider_user_project.config_data["gcp_project_name"]}.
            Please ensure, that the service account {provider_user_project.config_data["gcp_service_account_email"]} has the owner role on the project.
            """
            raise ProviderUserProjectConfigurationError(error_message) from error

    def _grant_serviceusage_admin_role_to_service_account(
        self, credentials: Credentials, provider_user_project: ProviderUserProject
    ) -> None:
        try:
            self._gcp_project_iam_role_grant_service.grant_role_to_service_account(
                credentials,
                provider_user_project.config_data["gcp_project_id"],
                provider_user_project.config_data["gcp_service_account_email"],
                "roles/serviceusage.serviceUsageAdmin",
            )
        except Exception as error:
            logger.warning(
                f"Unable to grant serviceusage admin role to service account for provider user project: {provider_user_project.id}. Error: {str(error)}"
            )
            error_message = f"""
            We were not able to grant serviceusage admin role to the service account {provider_user_project.config_data["gcp_service_account_email"]} on the project {provider_user_project.config_data["gcp_project_name"]}.
            Please ensure, that the service account {provider_user_project.config_data["gcp_service_account_email"]} has the owner role on the project."""
            raise ProviderUserProjectConfigurationError(error_message) from error

    def _check_billing_is_enabled(self, credentials: Credentials, provider_user_project: ProviderUserProject) -> None:
        try:
            billing_info = self._gcp_project_billing_info_get_service.get(
                credentials,
                provider_user_project.config_data["gcp_project_id"],
            )
        except Exception as error:
            logger.warning(
                f"Unable to get billing info for provider user project: {provider_user_project.id}. Error: {str(error)}"
            )
            error_message = f"""
            We were not able to get billing info for the project {provider_user_project.config_data["gcp_project_name"]}.
            Please ensure, that the billing is enabled for the project and the service account {provider_user_project.config_data["gcp_service_account_email"]} has the owner role on the project."""
            raise ProviderUserProjectConfigurationError(error_message) from error

        if not billing_info.billing_enabled:
            error_message = f"""
            The billing is not enabled for the project {provider_user_project.config_data["gcp_project_name"]}.
            Please enable billing for the project and then retry the verification process again."""
            raise ProviderUserProjectConfigurationError(error_message)

    @override
    @transaction.atomic
    def configure(self, provider_user_project: ProviderUserProject) -> ProviderUserProject:
        logger.info(
            "Configuring GCP project for provider user project: %(provider_user_project_id)s",
            {
                "provider_user_project_id": provider_user_project.id,
            },
        )

        credentials = self._create_credentials(provider_user_project)
        self._enable_project_apis(credentials, provider_user_project)
        self._grant_impersonation_to_service_accounts(credentials, provider_user_project)
        self._grant_serviceusage_admin_role_to_service_account(credentials, provider_user_project)
        self._check_billing_is_enabled(credentials, provider_user_project)

        logger.info(
            "GCP project configured successfully for provider user project: %(provider_user_project_id)s",
            {
                "provider_user_project_id": provider_user_project.id,
            },
        )
        return provider_user_project
