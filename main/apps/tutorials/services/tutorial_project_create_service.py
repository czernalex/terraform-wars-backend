import logging

from injector import inject
from django.db import transaction
from django.utils.translation import gettext as _
from ninja.errors import ValidationError

from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.models import TutorialProject
from main.apps.tutorials.schemas import CreateTutorialProjectSchema
from main.apps.tutorials.services.tutorial_project_configurator_factory import TutorialProjectConfiguratorFactory
from main.apps.tutorials.services.tutorial_project_retrieval_service import TutorialProjectRetrievalService
from main.apps.tutorials.services.tutorial_retrieval_service import TutorialRetrievalService
from main.apps.users.models import User


logger = logging.getLogger(__name__)


class TutorialProjectCreateService:
    @inject
    def __init__(
        self,
        tutorial_retrieval_service: TutorialRetrievalService,
        tutorial_project_retrieval_service: TutorialProjectRetrievalService,
        tutorial_project_configurator_factory: TutorialProjectConfiguratorFactory,
    ):
        self._tutorial_retrieval_service = tutorial_retrieval_service
        self._tutorial_project_configurator_factory = tutorial_project_configurator_factory

    @transaction.atomic
    def create(self, user: User, data: CreateTutorialProjectSchema) -> TutorialProject:
        try:
            tutorial = self._tutorial_retrieval_service.get_detail_by_id(data.tutorial_id)
        except NotFoundError:
            logger.warning(f"Tutorial: {data.tutorial_id} not found")
            raise ValidationError(
                [
                    {
                        "loc": ["tutorial_id"],
                        "msg": _("Tutorial not found"),
                        "type": "value_error",
                    }
                ]
            )

        logger.info(f"Creating tutorial project for user: {user.email} and tutorial: {tutorial.title}")
        tutorial_project = TutorialProject.objects.create(
            tutorial=tutorial,
            user=user,
        )
        logger.info(f"Tutorial project created successfully for user: {user.email} and tutorial: {tutorial.title}")

        configurator = self._tutorial_project_configurator_factory.get_configurator(tutorial_project)
        configurator.configure(tutorial_project)
        logger.info(f"Tutorial project configured successfully for user: {user.email} and tutorial: {tutorial.title}")

        return tutorial_project
