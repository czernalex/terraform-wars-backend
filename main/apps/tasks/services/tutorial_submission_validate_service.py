import logging
from uuid import UUID

from django.conf import settings
from injector import inject

from main.apps.gcp.services import GCPCloudRunJobInvokeService
from main.apps.tasks.services.validator_environment_configurator import ValidatorEnvironmentConfigurator
from main.apps.tasks.services.validator_environment_configurator_factory import ValidatorEnvironmentConfiguratorFactory
from main.apps.tutorials.models import TutorialSubmission
from main.apps.tutorials.services import TutorialSubmissionRetrievalService


logger = logging.getLogger(__name__)


class TutorialSubmissionValidateService:
    @inject
    def __init__(
        self,
        tutorial_submission_retrieval_service: TutorialSubmissionRetrievalService,
        validator_environment_configurator_factory: ValidatorEnvironmentConfiguratorFactory,
        gcp_cloud_run_job_invoke_service: GCPCloudRunJobInvokeService,
    ):
        self._tutorial_submission_retrieval_service = tutorial_submission_retrieval_service
        self._validator_environment_configurator_factory = validator_environment_configurator_factory
        self._gcp_cloud_run_job_invoke_service = gcp_cloud_run_job_invoke_service

    def _invoke_validation_job(
        self,
        tutorial_submission: TutorialSubmission,
        environment_configurator: ValidatorEnvironmentConfigurator,
    ) -> None:
        logger.info(f"Invoking execution job for tutorial submission: {tutorial_submission.id}")
        self._gcp_cloud_run_job_invoke_service.invoke(
            job_name=settings.GCP_TERRAFORM_VALIDATOR_JOB_NAME,
            job_container_name="app-production-1",
            job_container_env_vars=environment_configurator.configure(tutorial_submission),
        )
        logger.info(f"Execution job for tutorial submission: {tutorial_submission.id} invoked successfully")

    def validate(self, tutorial_submission_id: UUID) -> None:
        tutorial_submission = self._tutorial_submission_retrieval_service.get_detail_by_id(tutorial_submission_id)
        environment_configurator = self._validator_environment_configurator_factory.get_configurator(
            tutorial_submission
        )
        self._invoke_validation_job(tutorial_submission, environment_configurator)
