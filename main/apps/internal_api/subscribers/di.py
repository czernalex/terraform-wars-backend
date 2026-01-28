from injector import Binder, Module, singleton

from main.apps.internal_api.subscribers.services import (
    PubSubMessageDataParser,
    TutorialSubmissionExecutionFinishedHandler,
    TutorialSubmissionValidationFinishedHandler,
)


class SubscribersModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(PubSubMessageDataParser, to=PubSubMessageDataParser, scope=singleton)
        binder.bind(
            TutorialSubmissionExecutionFinishedHandler, to=TutorialSubmissionExecutionFinishedHandler, scope=singleton
        )
        binder.bind(
            TutorialSubmissionValidationFinishedHandler, to=TutorialSubmissionValidationFinishedHandler, scope=singleton
        )
