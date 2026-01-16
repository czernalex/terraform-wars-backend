import logging

from ninja.errors import ValidationError

from main.apps.tutorials.models import TutorialProject
from main.apps.tutorials.enums import TutorialProjectStatus


logger = logging.getLogger(__name__)


class TutorialProjectValidationService:
    def validate_is_configured(self, tutorial_project: TutorialProject, loc: str = "tutorial_project_id") -> None:
        if tutorial_project.status == TutorialProjectStatus.CONFIGURED:
            return

        error_message = f"Tutorial project {tutorial_project.id} is not properly configured"
        logger.warning(error_message)
        raise ValidationError([{"loc": [loc], "msg": error_message, "type": "value_error"}])
