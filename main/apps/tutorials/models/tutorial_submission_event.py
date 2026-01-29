from typing import override
from uuid import UUID

from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel
from main.apps.tutorials.enums import TutorialSubmissionStatus
from main.apps.tutorials.managers import TutorialSubmissionEventQuerySet
from main.apps.tutorials.models.tutorial_submission import TutorialSubmission


class TutorialSubmissionEvent(AbstractUUIDModel):
    tutorial_submission = models.ForeignKey(TutorialSubmission, on_delete=models.CASCADE, related_name="events")
    tutorial_submission_id: UUID

    event_status = models.CharField(_("Event status"), max_length=255, choices=TutorialSubmissionStatus.choices)

    exit_code = models.IntegerField(_("Exit code"))
    stdout = models.TextField(_("Output"), blank=True, default="")
    error = models.TextField(_("Error"), blank=True, default="")

    objects = TutorialSubmissionEventQuerySet.as_manager()

    class Meta:
        verbose_name = _("Tutorial submission event")
        verbose_name_plural = _("Tutorial submission events")
        ordering = ("-created_at",)

    @override
    def __str__(self) -> str:
        return f"[{self.tutorial_submission.tutorial.title}:{self.event_status}] - {self.exit_code}"
