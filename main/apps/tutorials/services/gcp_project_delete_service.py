import logging

from google.cloud import resourcemanager_v3
from google.oauth2.credentials import Credentials


logger = logging.getLogger(__name__)


class GCPProjectDeleteService:
    def _get_projects_client(self, credentials: Credentials) -> resourcemanager_v3.ProjectsClient:
        return resourcemanager_v3.ProjectsClient(credentials=credentials)

    def _delete_project(self, client: resourcemanager_v3.ProjectsClient, project_name: str) -> None:
        delete_request = resourcemanager_v3.DeleteProjectRequest(name=project_name)
        logger.info(f"Deleting project: {project_name}")
        operation = client.delete_project(request=delete_request)
        operation.result()

    def delete(self, credentials: Credentials, project_name: str) -> None:
        client = self._get_projects_client(credentials)
        self._delete_project(client, project_name)
        logger.info(f"Successfully deleted project: {project_name}")
