import logging
from typing import Sequence

from google.cloud import resourcemanager_v3
from google.iam.v1 import iam_policy_pb2, policy_pb2
from google.oauth2.credentials import Credentials


logger = logging.getLogger(__name__)


class GCPProjectIamRoleGrantService:
    """
    Grants project-level IAM roles to a service account.

    Example use cases:
    - roles/serviceusage.serviceUsageAdmin (Terraform API enablement)
    """

    def _get_projects_client(self, credentials: Credentials) -> resourcemanager_v3.ProjectsClient:
        return resourcemanager_v3.ProjectsClient(credentials=credentials)

    def _ensure_role_binding(
        self,
        policy: policy_pb2.Policy,
        role: str,
        member: str,
        project_id: str,
    ) -> policy_pb2.Policy:
        for binding in policy.bindings:
            if binding.role == role:
                if member not in binding.members:
                    binding.members.append(member)
                    logger.info(f"Added {member} to {binding.role} binding for {project_id}")
                    break
        else:
            policy.bindings.append(
                policy_pb2.Binding(
                    role=role,
                    members=[member],
                )
            )
            logger.info(f"Created new {role} binding for {project_id} with member {member}")

        return policy

    def grant_role_to_service_account(
        self,
        credentials: Credentials,
        project_id: str,
        service_account_email: str,
        roles: Sequence[str],
    ) -> None:
        """
        Grants a project-level role to a service account.
        """
        client = self._get_projects_client(credentials)
        member = f"serviceAccount:{service_account_email}"

        logger.info(f"Granting {len(roles)} roles to {member} on {project_id}")

        policy = client.get_iam_policy(request=iam_policy_pb2.GetIamPolicyRequest(resource=f"projects/{project_id}"))

        for role in roles:
            policy = self._ensure_role_binding(
                policy=policy,
                role=role,
                member=member,
                project_id=project_id,
            )

        client.set_iam_policy(
            request=iam_policy_pb2.SetIamPolicyRequest(resource=f"projects/{project_id}", policy=policy)
        )
        logger.info(f"Successfully granted {len(roles)} roles to {member} on {project_id}")
