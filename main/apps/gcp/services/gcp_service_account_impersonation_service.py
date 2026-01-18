import logging

from google.cloud import iam_admin_v1
from google.iam.v1 import iam_policy_pb2, policy_pb2
from google.oauth2.credentials import Credentials


logger = logging.getLogger(__name__)


class GCPServiceAccountImpersonationService:
    """
    The responsibility of this service is to grant our service account (SA) roles/iam.serviceAccountTokenCreator
    role on the newly created service account (in the newly created GCP project).
    This will allow our SA to impersonate the newly created SA by using generateAccessToken, ADC, Terraform etc.
    """

    ROLE = "roles/iam.serviceAccountTokenCreator"

    def _get_iam_client(self, credentials: Credentials) -> iam_admin_v1.IAMClient:
        return iam_admin_v1.IAMClient(credentials=credentials)

    def _update_iam_policy(self, policy: policy_pb2.Policy, resource: str, member: str) -> policy_pb2.Policy:
        for binding in policy.bindings:
            if binding.role == self.ROLE:
                if member not in binding.members:
                    binding.members.append(member)
                    logger.info(f"Added {member} to {binding.role} binding for {resource}")
                    break
        else:
            policy.bindings.append(
                policy_pb2.Binding(
                    role=self.ROLE,
                    members=[member],
                )
            )
            logger.info(f"Created new {self.ROLE} binding for {resource} with member {member}")

        return policy

    def grant_impersonation(
        self,
        credentials: Credentials,
        user_project_id: str,
        user_service_account_email: str,
        tw_executor_service_account_email: str,
    ) -> None:
        client = self._get_iam_client(credentials)

        resource = f"projects/{user_project_id}/serviceAccounts/{user_service_account_email}"
        member = f"serviceAccount:{tw_executor_service_account_email}"

        logger.info(f"Granting {self.ROLE} role to {member} on {resource}")
        policy = client.get_iam_policy(request=iam_policy_pb2.GetIamPolicyRequest(resource=resource))
        policy = self._update_iam_policy(policy, resource, member)
        client.set_iam_policy(request=iam_policy_pb2.SetIamPolicyRequest(resource=resource, policy=policy))
        logger.info(f"Successfully granted {self.ROLE} role to {member} on {resource}")
