from typing import TYPE_CHECKING

from django.db import models


if TYPE_CHECKING:
    from main.apps.tutorials.models import Tutorial, TutorialStep, TutorialStepSubmission, TutorialTag


class TutorialQuerySet(models.QuerySet["Tutorial"]):
    pass


class TutorialStepQuerySet(models.QuerySet["TutorialStep"]):
    pass


class TutorialStepSubmissionQuerySet(models.QuerySet["TutorialStepSubmission"]):
    pass


class TutorialTagQuerySet(models.QuerySet["TutorialTag"]):
    pass
