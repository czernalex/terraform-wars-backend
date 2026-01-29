import logging
from uuid import UUID

from django.conf import settings
from django.db import transaction
from injector import inject

from main.apps.gcp.services import GCPCloudRunJobInvokeService
from main.apps.internal_api.tasks.services.validator_environment_configurator import ValidatorEnvironmentConfigurator
from main.apps.internal_api.tasks.services.validator_environment_configurator_factory import (
    ValidatorEnvironmentConfiguratorFactory,
)
from main.apps.tutorials.enums import TutorialSubmissionStatus
from main.apps.tutorials.models import TutorialSubmission
from main.apps.tutorials.schemas import CreateTutorialSubmissionEventSchema
from main.apps.tutorials.services import (
    TutorialSubmissionEventCreateService,
    TutorialSubmissionRetrievalService,
    TutorialSubmissionUpdateService,
    TutorialSubmissionValidationService,
)


logger = logging.getLogger(__name__)


class TutorialSubmissionValidateService:
    @inject
    def __init__(
        self,
        tutorial_submission_retrieval_service: TutorialSubmissionRetrievalService,
        tutorial_submission_validation_service: TutorialSubmissionValidationService,
        tutorial_submission_update_service: TutorialSubmissionUpdateService,
        tutorial_submission_event_create_service: TutorialSubmissionEventCreateService,
        validator_environment_configurator_factory: ValidatorEnvironmentConfiguratorFactory,
        gcp_cloud_run_job_invoke_service: GCPCloudRunJobInvokeService,
    ):
        self._tutorial_submission_retrieval_service = tutorial_submission_retrieval_service
        self._tutorial_submission_validation_service = tutorial_submission_validation_service
        self._tutorial_submission_update_service = tutorial_submission_update_service
        self._tutorial_submission_event_create_service = tutorial_submission_event_create_service
        self._validator_environment_configurator_factory = validator_environment_configurator_factory
        self._gcp_cloud_run_job_invoke_service = gcp_cloud_run_job_invoke_service

    def _invoke_validation_job(
        self,
        tutorial_submission: TutorialSubmission,
        environment_configurator: ValidatorEnvironmentConfigurator,
    ) -> None:
        logger.info(f"Invoking validation job for tutorial submission: {tutorial_submission.id}")
        self._gcp_cloud_run_job_invoke_service.invoke(
            job_name=settings.GCP_TERRAFORM_VALIDATOR_JOB_NAME,
            job_container_name="app-production-1",
            job_container_args=None,
            job_container_env_vars=environment_configurator.configure(tutorial_submission),
        )
        logger.info(f"Validation job for tutorial submission: {tutorial_submission.id} invoked successfully")

    def _create_tutorial_submission_event(self, tutorial_submission: TutorialSubmission) -> None:
        create_tutorial_submission_event_data = CreateTutorialSubmissionEventSchema(
            event_status=tutorial_submission.status,
            exit_code=0,
            stdout="",
            error="",
        )
        self._tutorial_submission_event_create_service.create(
            tutorial_submission_id=tutorial_submission.id,
            data=create_tutorial_submission_event_data,
        )

    @transaction.atomic
    def validate(self, tutorial_submission_id: UUID, user_id: UUID) -> None:
        tutorial_submission = self._tutorial_submission_retrieval_service.get_for_update_by_id(
            user_id, tutorial_submission_id
        )
        self._tutorial_submission_validation_service.validate_can_be_validated(tutorial_submission)
        tutorial_submission = self._tutorial_submission_update_service.update_status(
            tutorial_submission, TutorialSubmissionStatus.VALIDATING
        )
        self._create_tutorial_submission_event(tutorial_submission)
        environment_configurator = self._validator_environment_configurator_factory.get_configurator(
            tutorial_submission
        )
        transaction.on_commit(lambda: self._invoke_validation_job(tutorial_submission, environment_configurator))
