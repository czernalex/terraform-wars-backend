from injector import Binder, Module, singleton

from main.apps.providers.services import (
    DefaultProviderProjectListServiceFactory,
    DefaultProviderUserProjectConfigDataFormatterServiceFactory,
    DefaultProviderUserProjectConfiguratorFactory,
    GCPProjectListService,
    GCPProviderUserProjectConfigDataFormatterService,
    GCPProviderUserProjectConfigurator,
    ProviderProjectListServiceFactory,
    ProviderRetrievalService,
    ProviderUserProjectConfigDataFormatterServiceFactory,
    ProviderUserProjectConfiguratorFactory,
    ProviderUserProjectCreateService,
    ProviderUserProjectDeleteService,
    ProviderUserProjectRetrievalService,
    ProviderUserProjectUpdateService,
    ProviderUserProjectValidationService,
    ProviderUserProjectConfigureService,
)


class ProvidersModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(ProviderRetrievalService, to=ProviderRetrievalService, scope=singleton)
        binder.bind(ProviderUserProjectRetrievalService, to=ProviderUserProjectRetrievalService, scope=singleton)
        binder.bind(ProviderUserProjectCreateService, to=ProviderUserProjectCreateService, scope=singleton)
        binder.bind(GCPProviderUserProjectConfigurator, to=GCPProviderUserProjectConfigurator, scope=singleton)
        binder.bind(
            ProviderUserProjectConfiguratorFactory, to=DefaultProviderUserProjectConfiguratorFactory, scope=singleton
        )
        binder.bind(ProviderUserProjectValidationService, to=ProviderUserProjectValidationService, scope=singleton)
        binder.bind(ProviderUserProjectConfigureService, to=ProviderUserProjectConfigureService, scope=singleton)
        binder.bind(
            GCPProviderUserProjectConfigDataFormatterService,
            to=GCPProviderUserProjectConfigDataFormatterService,
            scope=singleton,
        )
        binder.bind(
            ProviderUserProjectConfigDataFormatterServiceFactory,
            to=DefaultProviderUserProjectConfigDataFormatterServiceFactory,
            scope=singleton,
        )
        binder.bind(ProviderUserProjectUpdateService, to=ProviderUserProjectUpdateService, scope=singleton)
        binder.bind(ProviderUserProjectDeleteService, to=ProviderUserProjectDeleteService, scope=singleton)
        binder.bind(GCPProjectListService, to=GCPProjectListService, scope=singleton)
        binder.bind(ProviderProjectListServiceFactory, to=DefaultProviderProjectListServiceFactory, scope=singleton)
