from django.contrib import admin
from django.db import models
from django.http import HttpRequest
from django.utils.translation import gettext as _
from unfold.contrib.filters.admin import (
    AutocompleteSelectFilter,
    AutocompleteSelectMultipleFilter,
    ChoicesDropdownFilter,
    RangeDateFilter,
)
from unfold.contrib.forms.widgets import WysiwygWidget

from main.apps.core.admin import BaseModelAdmin
from main.apps.tutorials.models import (
    Tutorial,
    TutorialSubmission,
    TutorialTag,
)


@admin.register(Tutorial)
class TutorialAdmin(BaseModelAdmin):
    list_display = ("title", "author", "provider", "status", "difficulty", "created_at", "updated_at")
    list_select_related = (
        "author",
        "provider",
    )
    list_filter = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
        ("author", AutocompleteSelectFilter),
        ("provider", AutocompleteSelectFilter),
        ("tags", AutocompleteSelectMultipleFilter),
        ("status", ChoicesDropdownFilter),
        ("difficulty", ChoicesDropdownFilter),
    )
    search_fields = (
        "id",
        "author__id",
        "author__email",
        "provider__id",
        "provider__name",
        "title",
        "description",
    )
    autocomplete_fields = (
        "author",
        "provider",
    )
    prepopulated_fields = {
        "slug": ("title",),
    }
    filter_horizontal = ("tags",)
    wysiwyg_fields = (
        "description",
        "assignment",
    )
    fieldsets = (
        (
            _("Tutorial information"),
            {
                "fields": (
                    "provider",
                    "title",
                    "slug",
                    "description",
                    "assignment",
                    "status",
                    "difficulty",
                )
            },
        ),
        (
            _("Configuration"),
            {
                "classes": [
                    "tab",
                ],
                "fields": (
                    "config_data",
                    "validation_script",
                    "code_template",
                ),
            },
        ),
        (
            _("Author"),
            {
                "classes": [
                    "tab",
                ],
                "fields": ("author",),
            },
        ),
        (
            _("Tags"),
            {
                "classes": [
                    "tab",
                ],
                "fields": ("tags",),
            },
        ),
        (
            _("Audit info"),
            {
                "classes": [
                    "tab",
                ],
                "fields": ("id", "created_at", "updated_at"),
            },
        ),
    )

    def formfield_for_dbfield(self, db_field: models.Field, request: HttpRequest, **kwargs) -> models.Field | None:
        if isinstance(db_field, models.TextField) and db_field.name in self.wysiwyg_fields:
            kwargs["widget"] = WysiwygWidget

        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(TutorialSubmission)
class TutorialSubmissionAdmin(BaseModelAdmin):
    pass


@admin.register(TutorialTag)
class TutorialTagAdmin(BaseModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    list_filter = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
    )
    search_fields = (
        "id",
        "name",
        "slug",
    )
    prepopulated_fields = {
        "slug": ("name",),
    }
    fieldsets = (
        (_("Tutorial tag information"), {"fields": ("name", "slug")}),
        (_("Audit info"), {"fields": ("id", "created_at", "updated_at")}),
    )
