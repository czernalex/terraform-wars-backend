from injector import Injector

from main.apps.tutorials.di import TutorialsModule
from main.apps.users.di import UsersModule


injector = Injector(
    [
        TutorialsModule(),
        UsersModule(),
    ]
)
