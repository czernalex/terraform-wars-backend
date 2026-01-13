import logging

from google.cloud import iam_admin_v1
from google.cloud.iam_admin_v1 import types
from google.oauth2.credentials import Credentials

from main.apps.tutorials.models import TutorialProject


logger = logging.getLogger(__name__)


class GCPServiceAccountCreateService:
    def _generate_service_account_id(self) -> str:
        return "tw-executor-sa"

    def _get_iam_client(self, credentials: Credentials) -> iam_admin_v1.IAMClient:
        return iam_admin_v1.IAMClient(credentials=credentials)

    def _create_service_account(self, credentials: Credentials, project_id: str) -> types.ServiceAccount:
        service_account_id = self._generate_service_account_id()
        client = self._get_iam_client(credentials)
        create_request = iam_admin_v1.CreateServiceAccountRequest(
            name=f"projects/{project_id}",
            account_id=service_account_id,
            service_account=types.ServiceAccount(
                display_name="Terraform Wars Executor",
                description="Service account for Terraform Wars Executor",
            ),
        )
        service_account = client.create_service_account(request=create_request)
        logger.info(
            f"Service account: {service_account_id} created successfully in google cloud for project: {project_id}"
        )
        return service_account

    def create(self, credentials: Credentials, project_id: str, tutorial_project: TutorialProject) -> str:
        service_account = self._create_service_account(credentials, project_id)
        tutorial_project.config_data["gcp_service_account_email"] = service_account.email
        tutorial_project.config_data["gcp_service_account_id"] = service_account.name
        tutorial_project.save()
        logger.info(f"Service account: {service_account.email} created successfully for project: {project_id}")
        return service_account.email
