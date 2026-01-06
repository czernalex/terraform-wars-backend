from typing import override

from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel
from main.apps.tutorials.models.tutorial_step import TutorialStep
from main.apps.tutorials.models.provider_project import ProviderProject
from main.apps.users.models.user import User


class TutorialStepSubmission(AbstractUUIDModel):
    tutorial_step = models.ForeignKey(TutorialStep, on_delete=models.CASCADE, related_name="submissions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    provider_project = models.ForeignKey(ProviderProject, on_delete=models.CASCADE, related_name="submissions")

    code = models.TextField(_("Code"))

    # TODO: Add a field for the output, monitor submission status, etc. Will be implemented later

    class Meta:
        verbose_name = _("Tutorial Step Submission")
        verbose_name_plural = _("Tutorial Step Submissions")
        ordering = ("-created_at",)

    @override
    def __str__(self) -> str:
        return f"[{self.tutorial_step.tutorial.title}:{self.tutorial_step.title}] - {self.user.email}"
