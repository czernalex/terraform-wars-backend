import logging

from uuid import UUID
from django.db import transaction
from injector import inject

from main.apps.tutorials.services.tutorial_project_resources_destroy_service_factory import (
    TutorialProjectResourcesDestroyServiceFactory,
)
from main.apps.tutorials.services.tutorial_project_retrieval_service import TutorialProjectRetrievalService
from main.apps.users.models import User


logger = logging.getLogger(__name__)


class TutorialProjectDeleteService:
    @inject
    def __init__(
        self,
        tutorial_project_retrieval_service: TutorialProjectRetrievalService,
        tutorial_project_resources_destroy_service_factory: TutorialProjectResourcesDestroyServiceFactory,
    ):
        self._tutorial_project_retrieval_service = tutorial_project_retrieval_service
        self._tutorial_project_resources_destroy_service_factory = tutorial_project_resources_destroy_service_factory

    @transaction.atomic
    def delete_tutorial_project(self, user: User, tutorial_project_id: UUID) -> None:
        raise NotImplementedError("Not implemented yet")

    @transaction.atomic
    def destroy_tutorial_project_resources(self, user: User, tutorial_project_id: UUID) -> None:
        tutorial_project = self._tutorial_project_retrieval_service.get_tutorial_project_for_update_by_id(
            user, tutorial_project_id
        )
        tutorial_project_resources_destroy_service = (
            self._tutorial_project_resources_destroy_service_factory.get_service(tutorial_project)
        )
        tutorial_project_resources_destroy_service.destroy(tutorial_project)
        tutorial_project.config_data = {}
        tutorial_project.save()
        logger.info(
            f"Tutorial project resources destroyed successfully for user: {user.email} and tutorial project: {tutorial_project.id}"
        )
