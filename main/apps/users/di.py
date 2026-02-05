from injector import Binder, Module, singleton

from main.apps.users.services import (
    UserRetrievalService,
    UserUpdateService,
    UserValidationService,
    UserDeleteService,
    UserStatsRetrievalService,
)


class UsersModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(UserRetrievalService, to=UserRetrievalService, scope=singleton)
        binder.bind(UserValidationService, to=UserValidationService, scope=singleton)
        binder.bind(UserUpdateService, to=UserUpdateService, scope=singleton)
        binder.bind(UserDeleteService, to=UserDeleteService, scope=singleton)
        binder.bind(UserStatsRetrievalService, to=UserStatsRetrievalService, scope=singleton)
