from injector import Binder, Module, singleton

from main.apps.internal_api.tasks.services import (
    DefaultExecutorEnvironmentConfiguratorFactory,
    DefaultValidatorEnvironmentConfiguratorFactory,
    ExecutorEnvironmentConfiguratorFactory,
    GoogleProviderValidatorEnvironmentConfigurator,
    TutorialSubmissionExecuteService,
    GoogleProviderExecutorEnvironmentConfigurator,
    TutorialSubmissionValidateService,
    ValidatorEnvironmentConfiguratorFactory,
)


class TasksModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(TutorialSubmissionExecuteService, to=TutorialSubmissionExecuteService, scope=singleton)
        binder.bind(
            ExecutorEnvironmentConfiguratorFactory, to=DefaultExecutorEnvironmentConfiguratorFactory, scope=singleton
        )
        binder.bind(
            GoogleProviderExecutorEnvironmentConfigurator,
            to=GoogleProviderExecutorEnvironmentConfigurator,
            scope=singleton,
        )
        binder.bind(
            ValidatorEnvironmentConfiguratorFactory, to=DefaultValidatorEnvironmentConfiguratorFactory, scope=singleton
        )
        binder.bind(
            GoogleProviderValidatorEnvironmentConfigurator,
            to=GoogleProviderValidatorEnvironmentConfigurator,
            scope=singleton,
        )
        binder.bind(TutorialSubmissionValidateService, to=TutorialSubmissionValidateService, scope=singleton)
