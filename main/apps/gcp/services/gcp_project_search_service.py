from typing import Iterator

from google.cloud.resourcemanager_v3.types import Project
from google.oauth2.credentials import Credentials
from google.cloud import resourcemanager_v3
from google.cloud.resourcemanager_v3.services.projects.pagers import SearchProjectsPager


class GCPProjectSearchService:
    def _get_projects_client(self, credentials: Credentials) -> resourcemanager_v3.ProjectsClient:
        return resourcemanager_v3.ProjectsClient(credentials=credentials)

    def _search_projects(self, client: resourcemanager_v3.ProjectsClient) -> SearchProjectsPager:
        search_request = resourcemanager_v3.SearchProjectsRequest(query="state:ACTIVE")
        return client.search_projects(request=search_request)

    def search(self, credentials: Credentials) -> Iterator[Project]:
        client = self._get_projects_client(credentials)
        projects_pager = self._search_projects(client)
        for project in projects_pager:
            yield project
