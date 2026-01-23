from injector import Injector

from main.apps.api_auth.di import ApiAuthModule
from main.apps.core.di import CoreModule
from main.apps.gcp.di import GCPModule
from main.apps.jobs.di import JobsModule
from main.apps.notifications.di import NotificationsModule
from main.apps.providers.di import ProvidersModule
from main.apps.tasks.di import TasksModule
from main.apps.tutorials.di import TutorialsModule
from main.apps.users.di import UsersModule


injector = Injector(
    [
        ApiAuthModule(),
        CoreModule(),
        GCPModule(),
        ProvidersModule(),
        JobsModule(),
        NotificationsModule(),
        TasksModule(),
        TutorialsModule(),
        UsersModule(),
    ]
)
