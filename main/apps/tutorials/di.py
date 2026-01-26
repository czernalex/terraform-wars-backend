from injector import Binder, Module, singleton

from main.apps.tutorials.services import (
    TutorialCreateService,
    TutorialRetrievalService,
    TutorialSubmissionRetrievalService,
    TutorialSubmissionCreateService,
    TutorialTagRetrievalService,
    TutorialValidationService,
)


class TutorialsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(TutorialRetrievalService, to=TutorialRetrievalService, scope=singleton)
        binder.bind(TutorialCreateService, to=TutorialCreateService, scope=singleton)
        binder.bind(TutorialTagRetrievalService, to=TutorialTagRetrievalService, scope=singleton)
        binder.bind(TutorialSubmissionRetrievalService, to=TutorialSubmissionRetrievalService, scope=singleton)
        binder.bind(TutorialSubmissionCreateService, to=TutorialSubmissionCreateService, scope=singleton)
        binder.bind(TutorialValidationService, to=TutorialValidationService, scope=singleton)
