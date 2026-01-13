import logging

from google.cloud import iam_admin_v1
from google.iam.v1 import iam_policy_pb2, policy_pb2
from google.oauth2.credentials import Credentials


logger = logging.getLogger(__name__)


class GCPProjectIamRoleGrantService:
    """
    Grants project-level IAM roles to a service account.

    Example use cases:
    - roles/serviceusage.serviceUsageAdmin (Terraform API enablement)
    """

    def _get_iam_client(self, credentials: Credentials) -> iam_admin_v1.IAMClient:
        return iam_admin_v1.IAMClient(credentials=credentials)

    def _ensure_role_binding(
        self,
        policy: policy_pb2.Policy,
        role: str,
        member: str,
        project_name: str,
    ) -> policy_pb2.Policy:
        for binding in policy.bindings:
            if binding.role == role:
                if member not in binding.members:
                    binding.members.append(member)
                    logger.info(f"Added {member} to {binding.role} binding for {project_name}")
                    break
        else:
            policy.bindings.append(
                policy_pb2.Binding(
                    role=role,
                    members=[member],
                )
            )
            logger.info(f"Created new {role} binding for {project_name} with member {member}")

        return policy

    def grant_role_to_service_account(
        self,
        credentials: Credentials,
        project_name: str,
        service_account_email: str,
        role: str,
    ) -> None:
        """
        Grants a project-level role to a service account.
        """
        client = self._get_iam_client(credentials)
        member = f"serviceAccount:{service_account_email}"

        policy = client.get_iam_policy(request=iam_policy_pb2.GetIamPolicyRequest(resource=project_name))

        policy = self._ensure_role_binding(
            policy=policy,
            role=role,
            member=member,
            project_name=project_name,
        )

        client.set_iam_policy(request=iam_policy_pb2.SetIamPolicyRequest(resource=project_name, policy=policy))
        logger.info(f"Successfully granted {role} to {member} on {project_name}")
