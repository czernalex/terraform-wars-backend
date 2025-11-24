from typing import override

from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel
from main.apps.tutorials.models.tutorial import Tutorial


class TutorialStep(AbstractUUIDModel):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name="steps")
    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.TextField(_("Description"))

    order = models.PositiveIntegerField(
        _("Order"),
        default=100,
        help_text=_("The order of the step in the tutorial"),
    )

    class Meta:
        verbose_name = _("Tutorial Step")
        verbose_name_plural = _("Tutorial Steps")
        ordering = ("order",)

    @override
    def __str__(self) -> str:
        return f"[{self.tutorial.title}] - {self.order}. {self.title}"
