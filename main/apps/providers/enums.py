from django.db import models
from django.utils.translation import gettext_lazy as _


class ProviderUserProjectStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    CONFIGURED = "configured", _("Configured")
    FAILED = "failed", _("Failed")
