from typing import override
from uuid import UUID

from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel
from main.apps.tutorials.enums import TutorialVoteValue
from main.apps.tutorials.managers import TutorialVoteQuerySet
from main.apps.tutorials.models.tutorial import Tutorial
from main.apps.users.models.user import User


class TutorialVote(AbstractUUIDModel):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="votes")
    tutorial_id: UUID
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    user_id: UUID

    vote_value = models.IntegerField(_("Vote"), choices=TutorialVoteValue.choices)

    objects = TutorialVoteQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tutorial", "user"], name="unique_tutorial_user_vote"),
        ]
        verbose_name = _("Tutorial Vote")
        verbose_name_plural = _("Tutorial Votes")
        ordering = ("-created_at",)

    @override
    def __str__(self) -> str:
        return f"[{self.tutorial.title}]:{self.user.email} -> {self.vote_value}"
