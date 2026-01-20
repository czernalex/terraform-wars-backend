from typing import override
from uuid import UUID

from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel
from main.apps.providers.models.provider import Provider
from main.apps.tutorials.enums import Difficulty, TutorialStatus
from main.apps.tutorials.managers import TutorialQuerySet
from main.apps.tutorials.models.tutorial_tag import TutorialTag
from main.apps.users.models import User


class Tutorial(AbstractUUIDModel):
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, related_name="tutorials")
    provider_id: UUID
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tutorials")
    author_id: UUID

    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.TextField(_("Description"))
    assignment = models.TextField(_("Assignment"))
    tags = models.ManyToManyField(TutorialTag, related_name="tutorials", blank=True)
    status = models.CharField(
        _("Status"),
        max_length=255,
        choices=TutorialStatus.choices,
        default=TutorialStatus.DRAFT,
    )
    difficulty = models.CharField(
        _("Difficulty"),
        max_length=255,
        choices=Difficulty.choices,
        default=Difficulty.BEGINNER,
    )

    config_data = models.JSONField(_("Config data"), default=dict)

    validation_script = models.TextField(
        _("Validation script"),
        help_text=_("Validates resources managed by the terraform code"),
    )
    code_template = models.TextField(
        _("Code template"),
        blank=True,
        default="",
        help_text=_("What the user will see when they start the tutorial"),
    )

    objects = TutorialQuerySet.as_manager()

    class Meta:
        indexes = [GinIndex(fields=["config_data"])]
        verbose_name = _("Tutorial")
        verbose_name_plural = _("Tutorials")
        ordering = ("-created_at",)

    @override
    def __str__(self) -> str:
        return f"[{self.provider.provider_id}] - {self.title}"
