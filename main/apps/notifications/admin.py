from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import (
    AutocompleteSelectFilter,
    BooleanRadioFilter,
    ChoicesDropdownFilter,
    RangeDateFilter,
)

from main.apps.core.admin import BaseModelAdmin
from main.apps.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(BaseModelAdmin):
    list_display = ("user", "text", "level", "dispatched", "created_at", "updated_at")
    list_select_related = ("user",)
    list_filter = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
        ("user", AutocompleteSelectFilter),
        ("level", ChoicesDropdownFilter),
        ("dispatched", BooleanRadioFilter),
    )
    search_fields = (
        "id",
        "user__id",
        "user__email",
        "text",
        "level",
    )
    autocomplete_fields = ("user",)
    fieldsets = (
        (
            _("Notification information"),
            {
                "fields": (
                    "user",
                    "text",
                    "level",
                    "dispatched",
                )
            },
        ),
        (_("Audit info"), {"fields": ("id", "created_at", "updated_at")}),
    )
