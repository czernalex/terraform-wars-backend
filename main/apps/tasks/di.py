from injector import Binder, Module, singleton

from main.apps.tasks.services import (
    DefaultExecutorEnvironmentConfiguratorFactory,
    ExecutorEnvironmentConfiguratorFactory,
    TutorialSubmissionExecuteService,
    GoogleProviderExecutorEnvironmentConfigurator,
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
