import logging
from typing import MutableSequence

from google.oauth2.credentials import Credentials
from google.cloud import run_v2


logger = logging.getLogger(__name__)


class GCPCloudRunJobInvokeService:
    def _get_jobs_client(self, credentials: Credentials) -> run_v2.JobsClient:
        return run_v2.JobsClient(credentials=credentials)

    def _run_job(
        self,
        client: run_v2.JobsClient,
        job_name: str,
        job_container_name: str,
        job_container_env_vars: MutableSequence[run_v2.EnvVar],
    ) -> run_v2.Job:
        logger.info(f"Invoking Cloud Run Job: {job_name}")

        run_job_request = run_v2.RunJobRequest(
            name=job_name,
            overrides=run_v2.RunJobRequest.Overrides(
                container_overrides=[
                    run_v2.RunJobRequest.Overrides.ContainerOverride(
                        name=job_container_name,
                        env=job_container_env_vars,
                    ),
                ],
            ),
        )

        operation = client.run_job(request=run_job_request)
        operation.result()

        logger.info(f"Cloud Run Job: {job_name} invoked successfully")

    def invoke(
        self,
        credentials: Credentials,
        job_name: str,
        job_container_name: str,
        job_container_env_vars: MutableSequence[run_v2.EnvVar],
    ) -> None:
        client = self._get_jobs_client(credentials)
        self._run_job(client, job_name, job_container_name, job_container_env_vars)
