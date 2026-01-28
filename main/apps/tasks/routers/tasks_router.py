from http import HTTPStatus
from uuid import UUID

from django.http import HttpRequest
from ninja import Router

from main.apps.providers.schemas import ConfigureProviderUserProjectSchema
from main.apps.providers.services import ProviderUserProjectConfigureService
from main.apps.tasks.services import TutorialSubmissionExecuteService, TutorialSubmissionValidateService
from main.apps.tutorials.schemas import ExecuteTutorialSubmissionSchema, ValidateTutorialSubmissionSchema
from main.di import injector


tasks_router = Router()


@tasks_router.post(
    "/provider-user-projects/{provider_user_project_id}/configuration/",
    url_name="provider_user_project_configuration_list",
    response={HTTPStatus.NO_CONTENT: None},
    description="Verify a provider user project configuration",
)
def configure_provider_user_project(
    request: HttpRequest, provider_user_project_id: UUID, data: ConfigureProviderUserProjectSchema
) -> None:
    provider_user_project_configure_service = injector.get(ProviderUserProjectConfigureService)
    provider_user_project_configure_service.configure(data.user_id, provider_user_project_id)


@tasks_router.post(
    "/submissions/{tutorial_submission_id}/execute/",
    url_name="tutorial_submission_execute",
    response={HTTPStatus.NO_CONTENT: None},
    description="Trigger a tutorial submission execution",
)
def execute_tutorial_submission(
    request: HttpRequest,
    tutorial_submission_id: UUID,
    data: ExecuteTutorialSubmissionSchema,
) -> None:
    tutorial_submission_execution_service = injector.get(TutorialSubmissionExecuteService)
    tutorial_submission_execution_service.execute(tutorial_submission_id, data.user_id)


@tasks_router.post(
    "/submissions/{tutorial_submission_id}/validate/",
    url_name="tutorial_submission_validate",
    response={HTTPStatus.NO_CONTENT: None},
    description="Trigger a tutorial submission validation",
)
def validate_tutorial_submission(
    request: HttpRequest,
    tutorial_submission_id: UUID,
    data: ValidateTutorialSubmissionSchema,
) -> None:
    tutorial_submission_validate_service = injector.get(TutorialSubmissionValidateService)
    tutorial_submission_validate_service.validate(tutorial_submission_id, data.user_id)
