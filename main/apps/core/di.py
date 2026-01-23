from injector import Binder, Module, singleton

from main.apps.core.services import HeartbeatEventBuilder


class CoreModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(HeartbeatEventBuilder, to=HeartbeatEventBuilder, scope=singleton)
