from typing import override

from google.cloud import run_v2

from main.apps.internal_api.tasks.services.executor_environment_configurator import ExecutorEnvironmentConfigurator
from main.apps.tutorials.models import TutorialSubmission


class GoogleProviderExecutorEnvironmentConfigurator(ExecutorEnvironmentConfigurator):
    @override
    def configure(self, tutorial_submission: TutorialSubmission) -> list[run_v2.EnvVar]:
        provider_user_project = tutorial_submission.provider_user_project
        return [
            run_v2.EnvVar(name="USER_ID", value=str(tutorial_submission.user_id)),
            run_v2.EnvVar(name="TUTORIAL_ID", value=str(tutorial_submission.tutorial_id)),
            run_v2.EnvVar(name="TUTORIAL_SUBMISSION_ID", value=str(tutorial_submission.id)),
            run_v2.EnvVar(name="PROVIDER_USER_PROJECT_ID", value=str(provider_user_project.id)),
            run_v2.EnvVar(name="TF_CODE", value=tutorial_submission.code),
            run_v2.EnvVar(name="GOOGLE_PROJECT", value=provider_user_project.config_data["gcp_project_id"]),
            run_v2.EnvVar(name="GOOGLE_PROJECT_NAME", value=provider_user_project.config_data["gcp_project_name"]),
            run_v2.EnvVar(
                name="GOOGLE_IMPERSONATE_SERVICE_ACCOUNT",
                value=provider_user_project.config_data["gcp_service_account_email"],
            ),
        ]
