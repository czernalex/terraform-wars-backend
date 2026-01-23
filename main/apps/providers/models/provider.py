from typing import override

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractUUIDModel
from main.apps.providers.managers import ProviderQuerySet


class Provider(AbstractUUIDModel):
    provider_id = models.CharField(
        _("Provider ID"), max_length=255, help_text=_("Should match Allauth SocialApp provider")
    )
    name = models.CharField(_("Name"), max_length=255)
    short_name = models.CharField(_("Short Name"), max_length=16, blank=True, default="")
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.TextField(_("Description"))
    website_url = models.URLField(_("Website URL"))

    setup_instructions = models.TextField(
        _("Setup instructions"),
        help_text=_("Instructions on how to setup the Provider Project manually (e.g. through Console)"),
        blank=True,
        default="",
    )
    setup_script_instructions = models.TextField(
        _("Setup script instructions"),
        help_text=_("Instructions on how to setup the Provider Project using the setup script"),
        blank=True,
        default="",
    )
    setup_script = models.TextField(
        _("Setup script"),
        help_text=_("Script that utilizes the provider CLI to setup the Provider Project"),
        blank=True,
        default="",
    )
    setup_checklist = ArrayField(
        models.CharField(max_length=512), default=list, help_text=_("Checklist of steps to setup the Provider Project")
    )

    objects = ProviderQuerySet.as_manager()

    class Meta:
        verbose_name = _("Provider")
        verbose_name_plural = _("Providers")
        ordering = ("name",)

    @override
    def __str__(self) -> str:
        return self.name
