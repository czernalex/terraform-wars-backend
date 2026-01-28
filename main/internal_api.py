from http import HTTPStatus

from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpRequest, HttpResponse

from main.apps.core.exceptions import ForbiddenError, NotFoundError
from main.apps.core.schemas import ForbiddenErrorSchema, NotFoundErrorSchema
from main.apps.jobs.routers import jobs_router
from main.apps.tasks.routers import tasks_router
from main.terraform_wars_api import TerraformWarsAPI


root_internal_api_router = TerraformWarsAPI(
    title="Terraform Wars Internal API",
    urls_namespace="terraform-wars-internal-api",
    version="0.0.1",
    description=(
        "Internal RPC API for triggering Terraform Wars background tasks and other internal operations. Authentication is managed by Google Cloud IAM."
        "<br>"
        "<br>"
        "<a href='/api/docs' class='btn'>API Docs</a>"
        "<br>"
        "<a href='/events-api/docs' class='btn'>Events API Docs</a>"
        "<br>"
        "<br>"
        "<a href='/admin' class='btn'>Administration</a>"
    ),
    docs_decorator=staff_member_required if not settings.DEBUG else None,
    servers=[
        {"url": "http://localhost:8080", "description": "Local development server"},
        {"url": "https://api.app.terraformwars.com", "description": "Production server"},
        {
            "url": "https://terraform-wars-task-worker-production-436901077292.europe-west3.run.app",
            "description": "Production task worker server",
        },
    ],
    openapi_extra={
        "info": {
            "contact": {
                "email": "alexandrczerny@icloud.com",
            }
        }
    },
)


# Attach exception handlers


@root_internal_api_router.exception_handler(ForbiddenError)
def handle_forbidden_error(request: HttpRequest, exc: ForbiddenError) -> HttpResponse:
    return root_internal_api_router.create_response(
        request,
        data=ForbiddenErrorSchema(detail=str(exc)),
        status=HTTPStatus.FORBIDDEN,
    )


@root_internal_api_router.exception_handler(NotFoundError)
def handle_not_found_error(request: HttpRequest, exc: NotFoundError) -> HttpResponse:
    return root_internal_api_router.create_response(
        request,
        data=NotFoundErrorSchema(detail=str(exc)),
        status=HTTPStatus.NOT_FOUND,
    )


root_internal_api_router.add_router("/jobs", jobs_router, tags=["jobs"])
root_internal_api_router.add_router("/tasks", tasks_router, tags=["tasks"])
