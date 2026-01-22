from google.cloud import billing_v1
from google.auth.credentials import Credentials


class GCPProjectBillingInfoGetService:
    def _get_billing_client(self, credentials: Credentials) -> billing_v1.CloudBillingClient:
        return billing_v1.CloudBillingClient(credentials=credentials)

    def _get_project_billing_info(
        self, client: billing_v1.CloudBillingClient, project_id: str
    ) -> billing_v1.ProjectBillingInfo:
        get_request = billing_v1.GetProjectBillingInfoRequest(name=f"projects/{project_id}")
        return client.get_project_billing_info(request=get_request)

    def get(self, credentials: Credentials, project_id: str) -> billing_v1.ProjectBillingInfo:
        client = self._get_billing_client(credentials)
        return self._get_project_billing_info(client, project_id)
