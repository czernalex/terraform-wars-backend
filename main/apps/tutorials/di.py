from injector import Binder, Module, singleton

from main.apps.tutorials.services import (
    ProviderRetrievalService,
    TutorialRetrievalService,
    TutorialTagRetrievalService,
    TutorialStepRetrievalService,
    TutorialStepSubmissionService,
)


class TutorialsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(ProviderRetrievalService, to=ProviderRetrievalService, scope=singleton)
        binder.bind(TutorialRetrievalService, to=TutorialRetrievalService, scope=singleton)
        binder.bind(TutorialTagRetrievalService, to=TutorialTagRetrievalService, scope=singleton)
        binder.bind(TutorialStepRetrievalService, to=TutorialStepRetrievalService, scope=singleton)
        binder.bind(TutorialStepSubmissionService, to=TutorialStepSubmissionService, scope=singleton)
