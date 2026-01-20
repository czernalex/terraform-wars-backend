from django.db import models
from django.utils.translation import gettext as _


class TutorialStatus(models.TextChoices):
    DRAFT = "draft", _("Draft")
    REVIEW = "review", _("Review")
    PUBLISHED = "published", _("Published")
    ARCHIVED = "archived", _("Archived")


class Difficulty(models.TextChoices):
    BEGINNER = "beginner", _("Beginner")
    INTERMEDIATE = "intermediate", _("Intermediate")
    ADVANCED = "advanced", _("Advanced")
    EXPERT = "expert", _("Expert")
