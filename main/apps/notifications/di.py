from injector import Binder, Module, singleton

from main.apps.notifications.services import (
    NotificationRetrievalService,
    NotificationStreamService,
    NotificationUpdateService,
    NotificationEventBuilder,
)


class NotificationsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(NotificationRetrievalService, to=NotificationRetrievalService, scope=singleton)
        binder.bind(NotificationUpdateService, to=NotificationUpdateService, scope=singleton)
        binder.bind(NotificationStreamService, to=NotificationStreamService, scope=singleton)
        binder.bind(NotificationEventBuilder, to=NotificationEventBuilder, scope=singleton)
