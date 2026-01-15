import logging

from google.cloud import resourcemanager_v3
from google.cloud.resourcemanager_v3 import types
from google.oauth2.credentials import Credentials

from main.apps.tutorials.models import TutorialProject


logger = logging.getLogger(__name__)


class GCPProjectCreateService:
    def _generate_project_id(self, tutorial_project: TutorialProject) -> str:
        uuid_str = str(tutorial_project.id).replace("-", "")
        return f"tw-{uuid_str[:27]}"

    def _get_projects_client(self, credentials: Credentials) -> resourcemanager_v3.ProjectsClient:
        return resourcemanager_v3.ProjectsClient(credentials=credentials)

    def _create_project(
        self, client: resourcemanager_v3.ProjectsClient, tutorial_project: TutorialProject
    ) -> types.Project:
        # TODO: This is a long blocking operation, it would be definitely better to run it in a background task
        # or asynchronously, to avoid blocking the worker thread
        project_id = self._generate_project_id(tutorial_project)
        create_request = resourcemanager_v3.CreateProjectRequest(
            project=resourcemanager_v3.Project(
                project_id=project_id,
                display_name=f"TW {tutorial_project.tutorial.title[:27]}",
            ),
        )
        logger.info(f"Creating project: {project_id} for tutorial project: {tutorial_project.id}")
        operation = client.create_project(request=create_request)
        return operation.result()

    def create(self, credentials: Credentials, tutorial_project: TutorialProject) -> types.Project:
        client = self._get_projects_client(credentials)
        project = self._create_project(client, tutorial_project)
        tutorial_project.config_data["gcp_project_id"] = project.project_id
        tutorial_project.config_data["gcp_project_name"] = project.name
        tutorial_project.save()
        logger.info(f"Project: {project.project_id} created successfully for tutorial project: {tutorial_project.id}")
        return project
