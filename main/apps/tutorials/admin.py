from django.contrib import admin
from django.utils.translation import gettext as _
from unfold.contrib.filters.admin import (
    AutocompleteSelectFilter,
    AutocompleteSelectMultipleFilter,
    ChoicesDropdownFilter,
    RangeDateFilter,
)

from main.apps.core.admin import BaseModelAdmin
from main.apps.tutorials.models import (
    Provider,
    Tutorial,
    TutorialStep,
    TutorialStepSubmission,
    TutorialTag,
    TutorialProject,
)


@admin.register(Provider)
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
        (_("Provider information"), {"fields": ("name", "slug", "provider_id", "description", "website_url")}),
        (_("Audit info"), {"fields": ("id", "created_at", "updated_at")}),
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
    fieldsets = (
        (
            _("Tutorial information"),
            {
                "fields": (
                    "provider",
                    "title",
                    "slug",
                    "description",
                    "status",
                    "difficulty",
                    "config_data",
                )
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


@admin.register(TutorialStep)
class TutorialStepAdmin(BaseModelAdmin):
    list_display = (
        "title",
        "tutorial",
        "order",
        "created_at",
        "updated_at",
    )
    list_select_related = ("tutorial",)
    list_filter = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
        ("tutorial", AutocompleteSelectFilter),
    )
    search_fields = (
        "id",
        "tutorial__id",
        "tutorial__title",
        "title",
        "description",
    )
    autocomplete_fields = ("tutorial",)
    prepopulated_fields = {
        "slug": ("title",),
    }
    fieldsets = (
        (
            _("Tutorial step information"),
            {
                "fields": (
                    "tutorial",
                    "title",
                    "slug",
                    "description",
                    "assignment",
                    "order",
                    "code_skeleton",
                )
            },
        ),
        (_("Audit info"), {"fields": ("id", "created_at", "updated_at")}),
    )


@admin.register(TutorialStepSubmission)
class TutorialStepSubmissionAdmin(BaseModelAdmin):
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


@admin.register(TutorialProject)
class TutorialProjectAdmin(BaseModelAdmin):
    list_display = ("tutorial", "user", "status", "created_at", "updated_at")
    list_select_related = ("tutorial", "user")
    list_filter = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
        ("tutorial", AutocompleteSelectFilter),
        ("tutorial__provider", AutocompleteSelectFilter),
        ("user", AutocompleteSelectFilter),
        ("status", ChoicesDropdownFilter),
    )
    search_fields = (
        "id",
        "tutorial__id",
        "tutorial__title",
        "user__id",
        "user__email",
    )
    autocomplete_fields = ("tutorial", "user")
    fieldsets = (
        (_("Tutorial project information"), {"fields": ("tutorial", "user", "status", "config_data")}),
        (_("Audit info"), {"fields": ("id", "created_at", "updated_at")}),
    )
