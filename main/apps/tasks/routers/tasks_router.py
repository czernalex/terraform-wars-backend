from http import HTTPStatus
from uuid import UUID
from ninja import Router

from main.apps.core.types import AuthedHttpRequest


tasks_router = Router()


@tasks_router.post(
    "/submissions/{tutorial_step_submission_id}/executions/",
    url_name="tutorial_step_submission_execution_list",
    response={HTTPStatus.OK: None},
    description="Trigger a tutorial step submission execution",
)
def create_tutorial_step_submission_execution(
    request: AuthedHttpRequest,
    tutorial_step_submission_id: UUID,
) -> None:
    return None


# create google cloud project
# create service account
# allow our service account to impersonate the user's service account
# store the terraform state to gcs bucket
