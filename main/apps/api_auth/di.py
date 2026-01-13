from injector import Binder, Module, singleton

from main.apps.api_auth.services import (
    SocialAccountRetrievalService,
    SocialAppRetrievalService,
    SocialTokenRetrievalService,
)


class ApiAuthModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(SocialAppRetrievalService, to=SocialAppRetrievalService, scope=singleton)
        binder.bind(SocialAccountRetrievalService, to=SocialAccountRetrievalService, scope=singleton)
        binder.bind(SocialTokenRetrievalService, to=SocialTokenRetrievalService, scope=singleton)
