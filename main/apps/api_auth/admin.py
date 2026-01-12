from allauth.mfa.admin import Authenticator
from allauth.socialaccount.admin import SocialApp, SocialAccount, SocialToken
from django.contrib import admin
from unfold.contrib.filters.admin import AutocompleteSelectFilter, ChoicesDropdownFilter, RangeDateFilter

from main.apps.core.admin import BaseModelAdmin


admin.site.unregister(Authenticator)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)


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
    list_display = (
        "provider",
        "name",
    )
    search_fields = (
        "id",
        "provider",
        "provider_id",
        "name",
    )


@admin.register(SocialAccount)
class SocialAccountAdmin(BaseModelAdmin):
    readonly_fields = ("id",)
    list_display = (
        "user",
        "provider",
        "uid",
    )
    list_select_related = ("user",)
    search_fields = (
        "id",
        "user__id",
        "user__email",
    )
    autocomplete_fields = ("user",)


@admin.register(SocialToken)
class SocialTokenAdmin(BaseModelAdmin):
    formfield_overrides = {}
    readonly_fields = ("id",)
    list_display = (
        "app",
        "account",
        "expires_at",
        "token",
    )
    list_select_related = ("app", "account")
    search_fields = (
        "id",
        "app__id",
        "app__provider",
        "app__name",
    )
    autocomplete_fields = ("app", "account")
