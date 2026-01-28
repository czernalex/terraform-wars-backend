import logging
from uuid import UUID

from django.conf import settings
from django.db import transaction
from injector import inject

from main.apps.gcp.services import GCPCloudRunJobInvokeService
from main.apps.internal_api.tasks.services.executor_environment_configurator import ExecutorEnvironmentConfigurator
from main.apps.internal_api.tasks.services.executor_environment_configurator_factory import (
    ExecutorEnvironmentConfiguratorFactory,
)
from main.apps.tutorials.enums import TutorialSubmissionStatus
from main.apps.tutorials.models import TutorialSubmission
from main.apps.tutorials.services import (
    TutorialSubmissionRetrievalService,
    TutorialSubmissionUpdateService,
    TutorialSubmissionValidationService,
)


logger = logging.getLogger(__name__)


class TutorialSubmissionExecuteService:
    @inject
    def __init__(
        self,
        tutorial_submission_retrieval_service: TutorialSubmissionRetrievalService,
        tutorial_submission_validation_service: TutorialSubmissionValidationService,
        tutorial_submission_update_service: TutorialSubmissionUpdateService,
        executor_environment_configurator_factory: ExecutorEnvironmentConfiguratorFactory,
        gcp_cloud_run_job_invoke_service: GCPCloudRunJobInvokeService,
    ):
        self._tutorial_submission_retrieval_service = tutorial_submission_retrieval_service
        self._tutorial_submission_validation_service = tutorial_submission_validation_service
        self._tutorial_submission_update_service = tutorial_submission_update_service
        self._executor_environment_configurator_factory = executor_environment_configurator_factory
        self._gcp_cloud_run_job_invoke_service = gcp_cloud_run_job_invoke_service

    def _invoke_execution_job(
        self,
        tutorial_submission: TutorialSubmission,
        environment_configurator: ExecutorEnvironmentConfigurator,
    ) -> None:
        logger.info(f"Invoking execution job for tutorial submission: {tutorial_submission.id}")
        self._gcp_cloud_run_job_invoke_service.invoke(
            job_name=settings.GCP_TERRAFORM_EXECUTOR_JOB_NAME,
            job_container_name="app-production-1",
            job_container_args=[tutorial_submission.provider_id],
            job_container_env_vars=environment_configurator.configure(tutorial_submission),
        )
        logger.info(f"Execution job for tutorial submission: {tutorial_submission.id} invoked successfully")

    @transaction.atomic
    def execute(self, tutorial_submission_id: UUID, user_id: UUID) -> None:
        tutorial_submission = self._tutorial_submission_retrieval_service.get_for_update_by_id(
            user_id, tutorial_submission_id
        )
        self._tutorial_submission_validation_service.validate_can_be_executed(tutorial_submission)
        tutorial_submission = self._tutorial_submission_update_service.update_status(
            tutorial_submission, TutorialSubmissionStatus.EXECUTING
        )
        environment_configurator = self._executor_environment_configurator_factory.get_configurator(tutorial_submission)
        transaction.on_commit(lambda: self._invoke_execution_job(tutorial_submission, environment_configurator))
