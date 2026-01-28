from django.db import models
from django.utils.translation import gettext as _


class TutorialStatus(models.TextChoices):
    DRAFT = "draft", _("Draft")
    REVIEW = "review", _("Review")
    REJECTED = "rejected", _("Rejected")
    APPROVED = "approved", _("Approved")
    PUBLISHED = "published", _("Published")
    ARCHIVED = "archived", _("Archived")


class Difficulty(models.TextChoices):
    BEGINNER = "beginner", _("Beginner")
    INTERMEDIATE = "intermediate", _("Intermediate")
    ADVANCED = "advanced", _("Advanced")
    EXPERT = "expert", _("Expert")


class TutorialSubmissionStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    EXECUTING = "executing", _("Executing")
    EXECUTION_SUCCEEDED = "execution_succeeded", _("Execution Succeeded")
    EXECUTION_FAILED = "execution_failed", _("Execution Failed")
    VALIDATING = "validating", _("Validating")
    SUCCEEDED = "succeeded", _("Succeeded")
    FAILED = "failed", _("Failed")


class TutorialVoteValue(models.IntegerChoices):
    UPVOTE = 1, _("Upvote")
    DOWNVOTE = -1, _("Downvote")
