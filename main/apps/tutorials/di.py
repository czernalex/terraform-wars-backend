from injector import Binder, Module, singleton

from main.apps.tutorials.services import (
    DefaultTutorialProjectResourcesDestroyServiceFactory,
    GCPTutorialProjectConfigurator,
    GCPTutorialProjectResourcesDestroyService,
    ProviderRetrievalService,
    TutorialProjectDeleteService,
    TutorialProjectResourcesDestroyServiceFactory,
    TutorialRetrievalService,
    TutorialStepSubmissionRetrievalService,
    TutorialTagRetrievalService,
    TutorialStepRetrievalService,
    TutorialProjectCreateService,
    TutorialStepSubmissionCreateService,
    TutorialProjectConfiguratorFactory,
    DefaultTutorialProjectConfiguratorFactory,
)


class TutorialsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(ProviderRetrievalService, to=ProviderRetrievalService, scope=singleton)
        binder.bind(TutorialRetrievalService, to=TutorialRetrievalService, scope=singleton)
        binder.bind(TutorialTagRetrievalService, to=TutorialTagRetrievalService, scope=singleton)
        binder.bind(TutorialStepRetrievalService, to=TutorialStepRetrievalService, scope=singleton)
        binder.bind(TutorialProjectCreateService, to=TutorialProjectCreateService, scope=singleton)
        binder.bind(TutorialProjectDeleteService, to=TutorialProjectDeleteService, scope=singleton)
        binder.bind(TutorialStepSubmissionCreateService, to=TutorialStepSubmissionCreateService, scope=singleton)
        binder.bind(GCPTutorialProjectConfigurator, to=GCPTutorialProjectConfigurator, scope=singleton)
        binder.bind(
            GCPTutorialProjectResourcesDestroyService, to=GCPTutorialProjectResourcesDestroyService, scope=singleton
        )
        binder.bind(TutorialProjectConfiguratorFactory, to=DefaultTutorialProjectConfiguratorFactory, scope=singleton)
        binder.bind(
            TutorialProjectResourcesDestroyServiceFactory,
            to=DefaultTutorialProjectResourcesDestroyServiceFactory,
            scope=singleton,
        )
        binder.bind(TutorialStepSubmissionRetrievalService, to=TutorialStepSubmissionRetrievalService, scope=singleton)
