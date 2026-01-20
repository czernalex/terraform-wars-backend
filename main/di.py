from injector import Injector

from main.apps.api_auth.di import ApiAuthModule
from main.apps.gcp.di import GCPModule
from main.apps.jobs.di import JobsModule
from main.apps.providers.di import ProvidersModule
from main.apps.tasks.di import TasksModule
from main.apps.tutorials.di import TutorialsModule
from main.apps.users.di import UsersModule


injector = Injector(
    [
        ApiAuthModule(),
        GCPModule(),
        ProvidersModule(),
        JobsModule(),
        TasksModule(),
        TutorialsModule(),
        UsersModule(),
    ]
)
