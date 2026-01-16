import logging
from typing import Optional, override

from allauth.socialaccount.models import SocialToken
from django.conf import settings
from django.utils.translation import gettext as _
from injector import inject
from google.cloud.resourcemanager_v3.types import Project
from google.cloud.iam_admin_v1.types import ServiceAccount
from ninja.errors import ValidationError

from main.apps.api_auth.services import SocialAppRetrievalService, SocialTokenRetrievalService
from main.apps.gcp.services.gcp_credentials_create_service import GCPCredentialsCreateService
from main.apps.gcp.services.gcp_project_create_service import GCPProjectCreateService
from main.apps.gcp.services.gcp_project_delete_service import GCPProjectDeleteService
from main.apps.gcp.services.gcp_project_iam_role_grant_service import GCPProjectIamRoleGrantService
from main.apps.gcp.services.gcp_service_account_create_service import GCPServiceAccountCreateService
from main.apps.gcp.services.gcp_service_account_impersonation_service import GCPServiceAccountImpersonationService
from main.apps.gcp.services.gcp_service_enable_service import GCPServiceEnableService
from main.apps.tutorials.enums import TutorialProjectStatus
from main.apps.tutorials.services.tutorial_project_update_config_data_service import (
    TutorialProjectUpdateConfigDataService,
)
from main.apps.tutorials.services.tutorial_project_configurator import TutorialProjectConfigurator
from main.apps.tutorials.models import TutorialProject


logger = logging.getLogger(__name__)


class GCPTutorialProjectConfigurator(TutorialProjectConfigurator):
    """
    GCP configurator orchestrates following steps:
    - Create a GCP project on behalf of the user
    - Create a GCP service account in the newly created project
    - Grant our service account (SA) roles/iam.serviceAccountTokenCreator role on the newly created service account (SA)
    - Enable required APIs (specified by the tutorial) in the GCP project
    """

    BOOTSTRAP_APIS = [
        "cloudresourcemanager.googleapis.com",
        "serviceusage.googleapis.com",
        "iam.googleapis.com",
        "iamcredentials.googleapis.com",
        "sts.googleapis.com",
    ]

    @inject
    def __init__(
        self,
        social_app_retrieval_service: SocialAppRetrievalService,
        social_token_retrieval_service: SocialTokenRetrievalService,
        gcp_credentials_create_service: GCPCredentialsCreateService,
        gcp_project_create_service: GCPProjectCreateService,
        gcp_project_delete_service: GCPProjectDeleteService,
        gcp_service_enable_service: GCPServiceEnableService,
        gcp_service_account_create_service: GCPServiceAccountCreateService,
        gcp_service_account_impersonation_service: GCPServiceAccountImpersonationService,
        gcp_project_iam_role_grant_service: GCPProjectIamRoleGrantService,
        tutorial_project_update_config_data_service: TutorialProjectUpdateConfigDataService,
    ):
        super().__init__(social_app_retrieval_service, social_token_retrieval_service)
        self._gcp_credentials_create_service = gcp_credentials_create_service
        self._gcp_project_create_service = gcp_project_create_service
        self._gcp_project_delete_service = gcp_project_delete_service
        self._gcp_service_enable_service = gcp_service_enable_service
        self._gcp_service_account_create_service = gcp_service_account_create_service
        self._gcp_service_account_impersonation_service = gcp_service_account_impersonation_service
        self._gcp_project_iam_role_grant_service = gcp_project_iam_role_grant_service
        self._tutorial_project_update_config_data_service = tutorial_project_update_config_data_service

    @override
    def get_provider_id(self) -> str:
        return "google"

    @override
    def _get_social_token(self, tutorial_project: TutorialProject) -> SocialToken:
        social_token = super()._get_social_token(tutorial_project)
        if not social_token.token_secret:
            raise ValueError(_("Refresh token is missing"))
        return social_token

    @override
    def configure(self, tutorial_project: TutorialProject) -> TutorialProject:
        social_token = self._get_social_token(tutorial_project)
        project: Optional[Project] = None
        social_app = self._get_social_app()
        logger.info(f"Configuring GCP project for tutorial project: {tutorial_project.id}")
        try:
            credentials = self._gcp_credentials_create_service.create(
                social_token,
                social_app,
                settings.SOCIALACCOUNT_PROVIDERS[self.get_provider_id()]["SCOPE"],
            )
            project = self._gcp_project_create_service.create(credentials, tutorial_project)
            self._gcp_service_enable_service.enable(credentials, project.name, self.BOOTSTRAP_APIS)
            service_account: ServiceAccount = self._gcp_service_account_create_service.create(
                credentials, project.project_id, tutorial_project
            )
            self._gcp_service_account_impersonation_service.grant_impersonation(
                credentials,
                project.project_id,
                service_account.email,
                settings.GCP_TERRAFORM_EXECUTOR_SERVICE_ACCOUNT_EMAIL,
            )
            # Granting this role enables terrafrorm to enable APIs in the project
            self._gcp_project_iam_role_grant_service.grant_role_to_service_account(
                credentials,
                project.project_id,
                service_account.email,
                "roles/serviceusage.serviceUsageAdmin",
            )
            self._tutorial_project_update_config_data_service.update(
                tutorial_project,
                {
                    "gcp_project_id": project.project_id,
                    "gcp_project_name": project.name,
                    "gcp_service_account_email": service_account.email,
                    "gcp_service_account_id": service_account.name,
                },
                TutorialProjectStatus.CONFIGURED,
            )
        except BaseException as error:
            logger.error(f"Error configuring tutorial project: {tutorial_project.id}", exc_info=True)
            if project:
                self._gcp_project_delete_service.delete(credentials, project.name)
            raise ValidationError(
                [
                    {
                        "loc": ["tutorial_project"],
                        "msg": _("Error configuring GCP project"),
                        "type": "value_error",
                    }
                ]
            ) from error

        logger.info(f"GCP project configured successfully for tutorial project: {tutorial_project.id}")
        return tutorial_project
