from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel


class TutorialGroup(AbstractUUIDModel):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)

    class Meta:
        ordering = ("order",)
        verbose_name = _("Tutorial Group")
        verbose_name_plural = _("Tutorial Groups")

    def __str__(self) -> str:
        return self.title
