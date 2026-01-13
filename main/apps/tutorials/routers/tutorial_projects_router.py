from http import HTTPStatus
from uuid import UUID
from ninja import Router

from main.di import injector
from main.apps.core.types import AuthedHttpRequest
from main.apps.core.schemas import NotFoundErrorSchema
from main.apps.tutorials.models import TutorialProject
from main.apps.tutorials.schemas import CreateTutorialProjectSchema, TutorialProjectDetailSchema
from main.apps.tutorials.services import TutorialProjectCreateService, TutorialProjectRetrievalService


tutorial_projects_router = Router()


@tutorial_projects_router.post(
    "/",
    url_name="tutorial_project_list",
    response={HTTPStatus.CREATED: TutorialProjectDetailSchema},
    description="Create a new tutorial project for the authenticated user and the selected tutorial.",
)
def create_tutorial_project(request: AuthedHttpRequest, data: CreateTutorialProjectSchema) -> TutorialProject:
    tutorial_project_create_service = injector.get(TutorialProjectCreateService)
    return tutorial_project_create_service.create_tutorial_project(request.user, data)


@tutorial_projects_router.get(
    "/{tutorial_project_id}/",
    url_name="tutorial_project_detail",
    response={
        HTTPStatus.OK: TutorialProjectDetailSchema,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Get the detail of a tutorial project for the authenticated user and the selected tutorial.",
)
def get_tutorial_project_detail(request: AuthedHttpRequest, tutorial_project_id: UUID) -> TutorialProject:
    tutorial_project_retrieval_service = injector.get(TutorialProjectRetrievalService)
    return tutorial_project_retrieval_service.get_tutorial_project_detail(request.user, tutorial_project_id)
