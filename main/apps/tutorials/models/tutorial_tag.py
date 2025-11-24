from typing import override

from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel
from main.apps.tutorials.managers import TutorialTagQuerySet


class TutorialTag(AbstractUUIDModel):
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True)

    objects = TutorialTagQuerySet.as_manager()

    class Meta:
        verbose_name = _("Tutorial Tag")
        verbose_name_plural = _("Tutorial Tags")
        ordering = ("name",)

    @override
    def __str__(self) -> str:
        return self.name
