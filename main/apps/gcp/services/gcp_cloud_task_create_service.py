from datetime import timedelta
from typing import Optional

from injector import inject
import msgspec
from django.utils import timezone
from google.cloud import tasks_v2
from google.protobuf import duration_pb2, timestamp_pb2


class GCPCloudTaskCreateService:
    @inject
    def __init__(
        self,
        client: tasks_v2.CloudTasksClient,
        gcp_project_id: str,
        gcp_region: str,
        gcp_service_account_email: str,
        gcp_audience: str,
    ):
        self._client = client
        self._gcp_project_id = gcp_project_id
        self._gcp_region = gcp_region
        self._gcp_service_account_email = gcp_service_account_email
        self._gcp_audience = gcp_audience

    def _create_http_task_name(self, queue_id: str, task_id: Optional[str]) -> Optional[str]:
        if not task_id:
            return None
        return self._client.task_path(self._gcp_project_id, self._gcp_region, queue_id, task_id)

    def _construct_http_task(
        self,
        queue_id: str,
        url: str,
        payload: Optional[dict],
        task_id: Optional[str],
        scheduled_time_from_now_in_seconds: Optional[int],
        deadline_time_in_seconds: Optional[int],
    ) -> tasks_v2.Task:
        task = tasks_v2.Task(
            http_request=tasks_v2.HttpRequest(
                http_method=tasks_v2.HttpMethod.POST,
                url=url,
                body=msgspec.json.encode(payload) if payload else None,
                headers={
                    "Content-Type": "application/json",
                },
                oidc_token=tasks_v2.OidcToken(
                    service_account_email=self._gcp_service_account_email, audience=self._gcp_audience
                ),
            ),
            name=self._create_http_task_name(queue_id, task_id),
        )

        # Convert to an absolute Protobuf Timestamp
        if scheduled_time_from_now_in_seconds:
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(timezone.now() + timedelta(seconds=scheduled_time_from_now_in_seconds))
            task.schedule_time = timestamp

        # Convert to a Protobuf Duration
        if deadline_time_in_seconds:
            duration = duration_pb2.Duration()
            duration.FromSeconds(deadline_time_in_seconds)
            task.dispatch_deadline = duration

        return task

    def create(
        self,
        queue_id: str,
        url: str,
        payload: Optional[dict] = None,
        task_id: Optional[str] = None,
        scheduled_time_from_now_in_seconds: Optional[int] = None,
        deadline_time_in_seconds: Optional[int] = None,
    ) -> tasks_v2.Task:
        task = self._construct_http_task(
            queue_id, url, payload, task_id, scheduled_time_from_now_in_seconds, deadline_time_in_seconds
        )
        return self._client.create_task(
            tasks_v2.CreateTaskRequest(
                parent=self._client.queue_path(
                    self._gcp_project_id,
                    self._gcp_region,
                    queue_id,
                ),
                task=task,
            )
        )
