from typing import override
from uuid import UUID

from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel
from main.apps.tutorials.managers import TutorialStepSubmissionQuerySet
from main.apps.tutorials.models.tutorial_project import TutorialProject
from main.apps.tutorials.models.tutorial_step import TutorialStep
from main.apps.users.models.user import User


class TutorialStepSubmission(AbstractUUIDModel):
    tutorial_project = models.ForeignKey(TutorialProject, on_delete=models.CASCADE, related_name="submissions")
    tutorial_project_id: UUID
    tutorial_step = models.ForeignKey(TutorialStep, on_delete=models.CASCADE, related_name="submissions")
    tutorial_step_id: UUID
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    user_id: UUID

    code = models.TextField(_("Code"))

    # TODO: Add a field for the output, monitor submission status, etc. Will be implemented later

    objects = TutorialStepSubmissionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Tutorial Step Submission")
        verbose_name_plural = _("Tutorial Step Submissions")
        ordering = ("-created_at",)

    @override
    def __str__(self) -> str:
        return f"[{self.tutorial_step.tutorial.title}:{self.tutorial_step.title}] - {self.user.email}"

    @property
    def tutorial_id(self) -> UUID:
        return self.tutorial_step.tutorial_id

    @property
    def provider_id(self) -> str:
        return self.tutorial_step.tutorial.provider.provider_id
