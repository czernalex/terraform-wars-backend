from injector import Binder, Module, singleton

from main.apps.tutorials.services import (
    GCPCredentialsService,
    GCPProjectCreateService,
    GCPServiceAccountCreateService,
    GCPServiceAccountImpersonationService,
    ProviderRetrievalService,
    TutorialRetrievalService,
    TutorialTagRetrievalService,
    TutorialStepRetrievalService,
    TutorialProjectCreateService,
    GCPProjectDeleteService,
    TutorialStepSubmissionService,
    TutorialProjectConfiguratorFactory,
    DefaultTutorialProjectConfiguratorFactory,
    GCPTutorialProjectConfigurator,
    GCPServiceEnableService,
    GCPProjectIamRoleGrantService,
)


class TutorialsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(ProviderRetrievalService, to=ProviderRetrievalService, scope=singleton)
        binder.bind(TutorialRetrievalService, to=TutorialRetrievalService, scope=singleton)
        binder.bind(TutorialTagRetrievalService, to=TutorialTagRetrievalService, scope=singleton)
        binder.bind(TutorialStepRetrievalService, to=TutorialStepRetrievalService, scope=singleton)
        binder.bind(TutorialProjectCreateService, to=TutorialProjectCreateService, scope=singleton)
        binder.bind(TutorialStepSubmissionService, to=TutorialStepSubmissionService, scope=singleton)
        binder.bind(GCPTutorialProjectConfigurator, to=GCPTutorialProjectConfigurator, scope=singleton)
        binder.bind(TutorialProjectConfiguratorFactory, to=DefaultTutorialProjectConfiguratorFactory, scope=singleton)
        binder.bind(GCPCredentialsService, to=GCPCredentialsService, scope=singleton)
        binder.bind(GCPProjectCreateService, to=GCPProjectCreateService, scope=singleton)
        binder.bind(GCPProjectDeleteService, to=GCPProjectDeleteService, scope=singleton)
        binder.bind(GCPServiceAccountCreateService, to=GCPServiceAccountCreateService, scope=singleton)
        binder.bind(GCPServiceAccountImpersonationService, to=GCPServiceAccountImpersonationService, scope=singleton)
        binder.bind(GCPServiceEnableService, to=GCPServiceEnableService, scope=singleton)
        binder.bind(GCPProjectIamRoleGrantService, to=GCPProjectIamRoleGrantService, scope=singleton)
