import logging

from ninja.errors import ValidationError

from main.apps.tutorials.enums import TutorialStatus
from main.apps.tutorials.models import Tutorial


logger = logging.getLogger(__name__)


class TutorialValidationService:
    def validate_accepts_submissions(self, tutorial: Tutorial, loc: str = "tutorial_id") -> None:
        if not tutorial.status != TutorialStatus.PUBLISHED:
            error_message = f"Tutorial {tutorial.id} does not accept submissions"
            logger.warning(error_message)
            raise ValidationError(
                [
                    {
                        "loc": [loc],
                        "msg": error_message,
                        "type": "value_error",
                    }
                ]
            )
