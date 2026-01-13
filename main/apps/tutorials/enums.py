from django.db import models
from django.utils.translation import gettext as _


class TutorialStatus(models.TextChoices):
    DRAFT = "draft", _("Draft")
    PUBLISHED = "published", _("Published")
    ARCHIVED = "archived", _("Archived")


class Difficulty(models.TextChoices):
    BEGINNER = "beginner", _("Beginner")
    INTERMEDIATE = "intermediate", _("Intermediate")
    ADVANCED = "advanced", _("Advanced")
    EXPERT = "expert", _("Expert")


class TutorialProjectStatus(models.TextChoices):
    CREATED = "created", _("Created")
    IN_PROGRESS = "in_progress", _("In progress")
    COMPLETED = "completed", _("Completed")
    FAILED = "failed", _("Failed")
