from django.db import models

from main.apps.core.models import AbstractUUIDModel
from main.apps.tutorials.models import Tutorial
from main.apps.users.models import User


class UserTutorial(AbstractUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    # provider_project ->
