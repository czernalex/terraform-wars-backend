from http import HTTPStatus

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from ninja.security import django_auth
from ninja.throttling import AnonRateThrottle, AuthRateThrottle

from main.apps.api_auth.routers import auth_router
from main.apps.core.exceptions import ForbiddenError, NotFoundError
from main.apps.core.schemas import ForbiddenErrorSchema, NotFoundErrorSchema
from main.apps.notifications.routers import notifications_router
from main.apps.providers.routers import providers_router, provider_user_projects_router
from main.apps.tutorials.routers import (
    tutorial_tags_router,
    tutorials_router,
    tutorial_submissions_router,
)
from main.apps.users.routers import users_router
from main.terraform_wars_api import TerraformWarsAPI


root_api_router = TerraformWarsAPI(
    title="Terraform Wars API",
    urls_namespace="terraform-wars-api",
    version="0.0.1",
    description=(
        "REST API for Terraform Wars application."
        "<br>"
        "<br>"
        "Authentication is managed by Django Allauth operating in headless mode. It's Open API specification is available "
        f"<a href='{settings.BASE_URL}/_allauth/openapi.html' target='_blank'>here</a>."
        "<br>"
        "<br>"
        "<a href='/events-api/docs' class='btn'>Events API Docs</a>"
        "<br>"
        "<a href='/_internal-api/docs' class='btn'>Internal API Docs</a>"
        "<br>"
        "<br>"
        "<a href='/admin' class='btn'>Administration</a>"
    ),
    docs_decorator=staff_member_required if not settings.DEBUG else None,
    servers=[
        {"url": "http://localhost:8080", "description": "Local development server"},
        {"url": "https://api.app.terraformwars.com", "description": "Production API server"},
    ],
    auth=django_auth,
    throttle=[
        AnonRateThrottle(rate="10/s"),
        AuthRateThrottle(rate="100/s"),
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


@root_api_router.exception_handler(ForbiddenError)
def handle_forbidden_error(request: HttpRequest, exc: ForbiddenError) -> HttpResponse:
    return root_api_router.create_response(
        request,
        data=ForbiddenErrorSchema(detail=str(exc)),
        status=HTTPStatus.FORBIDDEN,
    )


@root_api_router.exception_handler(NotFoundError)
def handle_not_found_error(request: HttpRequest, exc: NotFoundError) -> HttpResponse:
    return root_api_router.create_response(
        request,
        data=NotFoundErrorSchema(detail=str(exc)),
        status=HTTPStatus.NOT_FOUND,
    )


root_api_router.add_router("/auth", auth_router, tags=["auth"])
root_api_router.add_router("/notifications", notifications_router, tags=["notifications"])
root_api_router.add_router("/providers", providers_router, tags=["providers"])
root_api_router.add_router("/provider-user-projects", provider_user_projects_router, tags=["provider-user-projects"])
root_api_router.add_router("/submissions", tutorial_submissions_router, tags=["submissions"])
root_api_router.add_router("/tutorials", tutorials_router, tags=["tutorials"])
root_api_router.add_router("/tutorial-tags", tutorial_tags_router, tags=["tutorial-tags"])
root_api_router.add_router("/users", users_router, tags=["users"])
