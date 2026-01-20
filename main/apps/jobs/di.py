from injector import Binder, Module, singleton

from main.apps.jobs.services import ProviderUserProjectConfigureScheduler


class JobsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(ProviderUserProjectConfigureScheduler, to=ProviderUserProjectConfigureScheduler, scope=singleton)
