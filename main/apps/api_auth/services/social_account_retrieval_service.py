import logging
from allauth.socialaccount.models import SocialAccount
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.users.models import User


logger = logging.getLogger(__name__)


class SocialAccountRetrievalService:
    def get_social_account_detail(self, user: User, provider: str) -> SocialAccount:
        try:
            return SocialAccount.objects.filter(user=user).get(provider=provider)
        except SocialAccount.DoesNotExist:
            logger.warning(f"Social account not found for user: {user.id} and provider: {provider}")
            raise NotFoundError(_("Social account not found"))
