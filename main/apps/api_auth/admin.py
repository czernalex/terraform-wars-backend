from allauth.mfa.admin import Authenticator
from django.contrib import admin
from unfold.admin import ModelAdmin


admin.site.unregister(Authenticator)


@admin.register(Authenticator)
class AuthenticatorAdmin(ModelAdmin):
    pass
