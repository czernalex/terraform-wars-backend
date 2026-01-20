from http import HTTPStatus

from django.http import HttpRequest
from ninja import Router

from main.apps.jobs.services import ProviderUserProjectConfigureScheduler
from main.di import injector


jobs_router = Router()


@jobs_router.post(
    "/provider-user-projects/configurations/",
    url_name="provider_user_projects_configurations_list",
    response={HTTPStatus.NO_CONTENT: None},
    description="Configure pending provider user projects",
)
def configure_provider_user_projects(request: HttpRequest) -> None:
    provider_user_project_configure_scheduler = injector.get(ProviderUserProjectConfigureScheduler)
    provider_user_project_configure_scheduler.schedule()
