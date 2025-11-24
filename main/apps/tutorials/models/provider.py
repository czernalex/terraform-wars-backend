from typing import override

from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel


class Provider(AbstractUUIDModel):
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.TextField(_("Description"))
    website_url = models.URLField(_("Website URL"))

    class Meta:
        verbose_name = _("Provider")
        verbose_name_plural = _("Providers")
        ordering = ("name",)

    @override
    def __str__(self) -> str:
        return self.name
