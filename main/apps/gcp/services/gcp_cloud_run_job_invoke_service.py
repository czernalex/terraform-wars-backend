import logging
from typing import MutableSequence

from google.cloud import run_v2
from injector import inject


logger = logging.getLogger(__name__)


class GCPCloudRunJobInvokeService:
    @inject
    def __init__(self, client: run_v2.JobsClient, gcp_project_id: str, gcp_region: str):
        self._client = client
        self._gcp_project_id = gcp_project_id
        self._gcp_region = gcp_region

    def _create_job_name(self, job_name: str) -> str:
        return self._client.job_path(self._gcp_project_id, self._gcp_region, job_name)

    def _run_job(
        self,
        job_name: str,
        job_container_name: str,
        job_container_args: MutableSequence[str],
        job_container_env_vars: MutableSequence[run_v2.EnvVar],
    ) -> run_v2.Job:
        logger.info(f"Invoking Cloud Run Job: {job_name}")
        run_job_request = run_v2.RunJobRequest(
            name=self._create_job_name(job_name),
            overrides=run_v2.RunJobRequest.Overrides(
                container_overrides=[
                    run_v2.RunJobRequest.Overrides.ContainerOverride(
                        name=job_container_name,
                        args=job_container_args,
                        env=job_container_env_vars,
                    ),
                ],
            ),
        )
        operation = self._client.run_job(request=run_job_request)
        operation.result()
        logger.info(f"Cloud Run Job: {job_name} invoked successfully")

    def invoke(
        self,
        job_name: str,
        job_container_name: str,
        job_container_args: MutableSequence[str],
        job_container_env_vars: MutableSequence[run_v2.EnvVar],
    ) -> None:
        return self._run_job(job_name, job_container_name, job_container_args, job_container_env_vars)
