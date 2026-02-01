from http import HTTPStatus

from django.http import HttpRequest
from ninja import Router

from main.apps.internal_api.jobs.services import (
    ProviderUserProjectConfigureScheduler,
    TutorialSubmissionReconciliationService,
)
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


@jobs_router.post(
    "/submissions/reconciliation/",
    url_name="tutorial_submissions_reconciliation_list",
    response={HTTPStatus.NO_CONTENT: None},
    description="Reconcile in progress tutorial submissions",
)
def reconcile_tutorial_submissions(request: HttpRequest) -> None:
    tutorial_submission_reconciliation_service = injector.get(TutorialSubmissionReconciliationService)
    tutorial_submission_reconciliation_service.reconcile()
