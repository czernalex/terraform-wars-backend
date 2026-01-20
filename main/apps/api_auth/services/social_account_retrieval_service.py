import logging
from uuid import UUID

from allauth.socialaccount.models import SocialAccount
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError


logger = logging.getLogger(__name__)


class SocialAccountRetrievalService:
    def get_detail_by_user_id_and_provider(self, user_id: UUID, provider: str) -> SocialAccount:
        try:
            return SocialAccount.objects.filter(user_id=user_id).get(provider=provider)
        except SocialAccount.DoesNotExist:
            logger.warning(f"Social account not found for user: {user_id} and provider: {provider}")
            raise NotFoundError(_("Social account not found"))
