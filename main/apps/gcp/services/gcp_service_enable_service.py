import logging
from typing import MutableSequence

from google.cloud import service_usage_v1
from google.oauth2.credentials import Credentials


logger = logging.getLogger(__name__)


class GCPServiceEnableService:
    def _get_service_usage_client(self, credentials: Credentials) -> service_usage_v1.ServiceUsageClient:
        return service_usage_v1.ServiceUsageClient(credentials=credentials)

    def _batch_enable_services(
        self, client: service_usage_v1.ServiceUsageClient, project_name: str, service_ids: MutableSequence[str]
    ) -> service_usage_v1.BatchEnableServicesResponse:
        create_request = service_usage_v1.BatchEnableServicesRequest(
            parent=project_name,
            service_ids=service_ids,
        )
        logger.info(f"Enabling services: {', '.join(service_ids)} for project: {project_name}")
        operation = client.batch_enable_services(request=create_request)
        result = operation.result()
        logger.info(f"Services: {', '.join(service_ids)} enabled successfully for project: {project_name}")
        return result

    def enable(
        self, credentials: Credentials, project_name: str, service_ids: MutableSequence[str]
    ) -> service_usage_v1.BatchEnableServicesResponse:
        client = self._get_service_usage_client(credentials)
        return self._batch_enable_services(client, project_name, service_ids)
