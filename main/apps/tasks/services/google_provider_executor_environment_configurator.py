from django.conf import settings
from google.cloud import run_v2

from main.apps.tasks.services.executor_environment_configurator import ExecutorEnvironmentConfigurator
from main.apps.tutorials.models import TutorialStepSubmission


class GoogleProviderExecutorEnvironmentConfigurator(ExecutorEnvironmentConfigurator):
    def configure(self, tutorial_step_submission: TutorialStepSubmission) -> list[run_v2.EnvVar]:
        tutorial_project = tutorial_step_submission.tutorial_project
        return [
            run_v2.EnvVar(name="USER_ID", value=str(tutorial_step_submission.user_id)),
            run_v2.EnvVar(name="TUTORIAL_ID", value=str(tutorial_project.tutorial_id)),
            run_v2.EnvVar(name="TUTORIAL_PROJECT_ID", value=str(tutorial_project.id)),
            run_v2.EnvVar(name="TUTORIAL_STEP_SUBMISSION_ID", value=str(tutorial_step_submission.id)),
            run_v2.EnvVar(name="GCP_TF_STATE_BUCKET_NAME", value=settings.GCS_BUCKET_NAME),
            run_v2.EnvVar(name="GCP_PROJECT_ID", value=tutorial_project.config_data["gcp_project_id"]),
            run_v2.EnvVar(
                name="GCP_SERVICE_ACCOUNT_EMAIL", value=tutorial_project.config_data["gcp_service_account_email"]
            ),
            run_v2.EnvVar(name="TF_CODE", value=tutorial_step_submission.code),
        ]
