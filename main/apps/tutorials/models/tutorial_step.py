from typing import override

from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel
from main.apps.tutorials.managers import TutorialStepQuerySet
from main.apps.tutorials.models.tutorial import Tutorial


class TutorialStep(AbstractUUIDModel):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="steps")
    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True)

    description = models.TextField(_("Description"), help_text=_("The brief description of the step"))
    assignment = models.TextField(_("Assignment"), help_text=_("Full assignment for the step"))
    code_skeleton = models.TextField(
        _("Code skeleton"), help_text=_("The skeleton of the code"), blank=True, default=""
    )

    order = models.PositiveIntegerField(
        _("Order"),
        default=100,
        help_text=_("The order of the step in the tutorial"),
    )

    objects = TutorialStepQuerySet.as_manager()

    class Meta:
        verbose_name = _("Tutorial Step")
        verbose_name_plural = _("Tutorial Steps")
        ordering = ("order",)

    @override
    def __str__(self) -> str:
        return f"[{self.tutorial.title}] - {self.order}. {self.title}"
