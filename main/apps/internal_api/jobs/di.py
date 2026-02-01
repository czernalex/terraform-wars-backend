from injector import Binder, Module, singleton

from main.apps.internal_api.jobs.services import (
    ProviderUserProjectConfigureScheduler,
    TutorialSubmissionReconciliationService,
)


class JobsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(ProviderUserProjectConfigureScheduler, to=ProviderUserProjectConfigureScheduler, scope=singleton)
        binder.bind(
            TutorialSubmissionReconciliationService, to=TutorialSubmissionReconciliationService, scope=singleton
        )
