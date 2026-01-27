from typing import override
from uuid import UUID

from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel
from main.apps.tutorials.managers import TutorialReviewQuerySet
from main.apps.tutorials.models.tutorial import Tutorial
from main.apps.users.models.user import User


class TutorialReview(AbstractUUIDModel):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="reviews")
    tutorial_id: UUID
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    user_id: UUID
    feedback = models.TextField(_("Review feedback"))

    objects = TutorialReviewQuerySet.as_manager()

    class Meta:
        verbose_name = _("Tutorial Review")
        verbose_name_plural = _("Tutorial Reviews")
        ordering = ("-created_at",)

    @override
    def __str__(self) -> str:
        return f"[{self.tutorial.title}]:{self.user.email}"
