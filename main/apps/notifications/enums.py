from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationLevel(models.TextChoices):
    INFO = "info", _("Info")
    SUCCESS = "success", _("Success")
    WARNING = "warning", _("Warning")
    ERROR = "error", _("Error")
