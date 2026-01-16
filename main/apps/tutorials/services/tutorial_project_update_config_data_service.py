import logging

from main.apps.tutorials.enums import TutorialProjectStatus
from main.apps.tutorials.models.tutorial_project import TutorialProject


logger = logging.getLogger(__name__)


class TutorialProjectUpdateConfigDataService:
    def update(
        self, tutorial_project: TutorialProject, data: dict[str, str], status: TutorialProjectStatus
    ) -> TutorialProject:
        tutorial_project.config_data = data
        tutorial_project.status = status
        tutorial_project.save()
        logger.info(
            f"Tutorial project config data and status updated successfully for tutorial project: {tutorial_project.id}"
        )
        return tutorial_project
