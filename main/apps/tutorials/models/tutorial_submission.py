from typing import override
from uuid import UUID

from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel
from main.apps.tutorials.managers import TutorialSubmissionQuerySet
from main.apps.tutorials.models.tutorial import Tutorial
from main.apps.tutorials.models.tutorial_project import TutorialProject
from main.apps.users.models.user import User


class TutorialSubmission(AbstractUUIDModel):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="submissions")
    tutorial_id: UUID
    tutorial_project = models.ForeignKey(TutorialProject, on_delete=models.CASCADE, related_name="submissions")
    tutorial_project_id: UUID
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    user_id: UUID

    code = models.TextField(_("Code"))

    # TODO: Add a field for the output, monitor submission status, etc. Will be implemented later

    objects = TutorialSubmissionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Tutorial Submission")
        verbose_name_plural = _("Tutorial Submissions")
        ordering = ("-created_at",)

    @override
    def __str__(self) -> str:
        return f"[{self.tutorial.title}] - {self.user.email}"

    @property
    def provider_id(self) -> str:
        return self.tutorial.provider.provider_id
