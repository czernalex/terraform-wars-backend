import logging
from allauth.socialaccount.models import SocialApp
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError


logger = logging.getLogger(__name__)


class SocialAppRetrievalService:
    def get_detail(self, provider: str) -> SocialApp:
        try:
            return SocialApp.objects.get(provider=provider)
        except SocialApp.DoesNotExist:
            logger.warning(f"Social app not found for provider: {provider}")
            raise NotFoundError(_("Social app not found"))
