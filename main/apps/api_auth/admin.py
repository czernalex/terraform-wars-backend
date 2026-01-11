from allauth.mfa.admin import Authenticator
from allauth.socialaccount.admin import SocialApp
from django.contrib import admin
from unfold.contrib.filters.admin import AutocompleteSelectFilter, ChoicesDropdownFilter, RangeDateFilter

from main.apps.core.admin import BaseModelAdmin


admin.site.unregister(Authenticator)
admin.site.unregister(SocialApp)


@admin.register(Authenticator)
class AuthenticatorAdmin(BaseModelAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "last_used_at",
    )
    list_display = ("user", "type", "created_at", "last_used_at")
    list_select_related = ("user",)
    list_filter = (
        ("user", AutocompleteSelectFilter),
        ("type", ChoicesDropdownFilter),
        ("created_at", RangeDateFilter),
        ("last_used_at", RangeDateFilter),
    )
    search_fields = (
        "id",
        "user__id",
        "user__email",
    )
    autocomplete_fields = ("user",)


@admin.register(SocialApp)
class SocialAppAdmin(BaseModelAdmin):
    readonly_fields = ("id",)
