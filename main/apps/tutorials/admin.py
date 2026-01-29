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
    TutorialReview,
    TutorialSubmission,
    TutorialSubmissionEvent,
    TutorialTag,
    TutorialVote,
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


@admin.register(TutorialReview)
class TutorialReviewAdmin(BaseModelAdmin):
    list_display = ("tutorial", "user", "created_at", "updated_at")
    list_select_related = (
        "tutorial",
        "user",
    )
    list_filter = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
        ("tutorial", AutocompleteSelectFilter),
        ("user", AutocompleteSelectFilter),
    )
    search_fields = (
        "id",
        "tutorial__id",
        "tutorial__title",
        "user__id",
        "user__email",
    )
    autocomplete_fields = (
        "tutorial",
        "user",
    )
    fieldsets = (
        (_("Tutorial review information"), {"fields": ("tutorial", "user", "feedback")}),
        (_("Audit info"), {"fields": ("id", "created_at", "updated_at")}),
    )
    wysiwyg_fields = ("feedback",)

    def formfield_for_dbfield(self, db_field: models.Field, request: HttpRequest, **kwargs) -> models.Field | None:
        if isinstance(db_field, models.TextField) and db_field.name in self.wysiwyg_fields:
            kwargs["widget"] = WysiwygWidget

        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(TutorialSubmission)
class TutorialSubmissionAdmin(BaseModelAdmin):
    list_display = ("tutorial", "user", "provider_user_project", "status", "created_at", "updated_at")
    list_select_related = (
        "tutorial",
        "user",
        "provider_user_project",
    )
    list_filter = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
        ("tutorial", AutocompleteSelectFilter),
        ("user", AutocompleteSelectFilter),
        ("provider_user_project", AutocompleteSelectFilter),
        ("status", ChoicesDropdownFilter),
    )
    search_fields = (
        "id",
        "tutorial__id",
        "tutorial__title",
        "user__id",
        "user__email",
        "provider_user_project__id",
        "provider_user_project__name",
        "provider_user_project__project_id",
    )
    autocomplete_fields = (
        "tutorial",
        "user",
        "provider_user_project",
    )
    fieldsets = (
        (
            _("Tutorial submission information"),
            {
                "fields": (
                    "tutorial",
                    "user",
                    "provider_user_project",
                    "code",
                    "status",
                )
            },
        ),
        (_("Audit info"), {"fields": ("id", "created_at", "updated_at")}),
    )


@admin.register(TutorialSubmissionEvent)
class TutorialSubmissionEventAdmin(BaseModelAdmin):
    list_display = (
        "tutorial_submission",
        "event_status",
        "exit_code",
        "created_at",
        "updated_at",
    )
    list_select_related = ("tutorial_submission",)
    list_filter = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
        ("tutorial_submission", AutocompleteSelectFilter),
        ("tutorial_submission__user", AutocompleteSelectFilter),
        ("event_status", ChoicesDropdownFilter),
    )
    search_fields = (
        "id",
        "tutorial_submission__id",
        "tutorial_submission__tutorial__id",
        "tutorial_submission__tutorial__title",
        "tutorial_submission__user__id",
        "tutorial_submission__user__email",
        "event_status",
    )
    autocomplete_fields = ("tutorial_submission",)
    fieldsets = (
        (
            _("Tutorial submission event information"),
            {"fields": ("tutorial_submission", "event_status", "exit_code", "stdout", "error")},
        ),
        (_("Audit info"), {"fields": ("id", "created_at", "updated_at")}),
    )


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


@admin.register(TutorialVote)
class TutorialVoteAdmin(BaseModelAdmin):
    list_display = ("tutorial", "user", "vote_value", "created_at", "updated_at")
    list_select_related = (
        "tutorial",
        "user",
    )
    list_filter = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
    )
    search_fields = (
        "id",
        "tutorial__id",
        "tutorial__title",
        "user__id",
        "user__email",
    )
    autocomplete_fields = (
        "tutorial",
        "user",
    )
