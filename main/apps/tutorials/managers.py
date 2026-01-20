from typing import TYPE_CHECKING

from django.db import models


if TYPE_CHECKING:
    from main.apps.tutorials.models import (
        Tutorial,
        TutorialSubmission,
        TutorialTag,
    )


class TutorialQuerySet(models.QuerySet["Tutorial"]):
    pass


class TutorialSubmissionQuerySet(models.QuerySet["TutorialSubmission"]):
    pass


class TutorialTagQuerySet(models.QuerySet["TutorialTag"]):
    pass
