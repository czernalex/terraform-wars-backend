from injector import Injector

from main.apps.google_cloud_tasks.di import GoogleCloudTasksModule
from main.apps.tutorials.di import TutorialsModule
from main.apps.users.di import UsersModule


injector = Injector(
    [
        GoogleCloudTasksModule(),
        TutorialsModule(),
        UsersModule(),
    ]
)
