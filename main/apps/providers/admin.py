from django.db import models
from django.http import HttpRequest
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import AutocompleteSelectFilter, RangeDateFilter
from unfold.contrib.forms.widgets import WysiwygWidget

from main.apps.core.admin import BaseModelAdmin
from main.apps.providers.models import Provider, ProviderUserProject


@admin.register(Provider)  # noqa: F821
class ProviderAdmin(BaseModelAdmin):
    list_display = ("name", "provider_id", "website_url", "created_at", "updated_at")
    list_filter = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
    )
    search_fields = (
        "id",
        "provider_id",
        "slug",
        "name",
        "description",
        "website_url",
    )
    prepopulated_fields = {
        "slug": ("name",),
    }
    fieldsets = (
        (
            _("Provider information"),
            {
                "fields": (
                    "name",
                    "slug",
                    "provider_id",
                    "description",
                    "website_url",
                    "setup_instructions",
                    "setup_script",
                )
            },
        ),
        (_("Audit info"), {"fields": ("id", "created_at", "updated_at")}),
    )
    wysiwyg_fields = ("setup_instructions",)

    def formfield_for_dbfield(self, db_field: models.Field, request: HttpRequest, **kwargs) -> models.Field | None:
        if isinstance(db_field, models.TextField) and db_field.name in self.wysiwyg_fields:
            kwargs["widget"] = WysiwygWidget

        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(ProviderUserProject)
class ProviderUserProjectAdmin(BaseModelAdmin):
    list_display = (
        "project_id",
        "name",
        "provider",
        "user",
        "status",
        "configuration_attempts",
        "created_at",
        "updated_at",
    )
    list_select_related = ("provider", "user")
    list_filter = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
        ("provider", AutocompleteSelectFilter),
        ("user", AutocompleteSelectFilter),
        ("status", AutocompleteSelectFilter),
    )
    search_fields = (
        "id",
        "provider__id",
        "provider__provider_id",
        "provider__name",
        "user__id",
        "user__email",
        "project_id",
        "name",
        "description",
    )
    autocomplete_fields = ("provider", "user")
    fieldsets = (
        (
            _("Provider user project information"),
            {
                "fields": (
                    "provider",
                    "user",
                    "status",
                    "configuration_attempts",
                    "project_id",
                    "name",
                    "description",
                    "config_data",
                )
            },
        ),
        (_("Audit info"), {"fields": ("id", "created_at", "updated_at")}),
    )
