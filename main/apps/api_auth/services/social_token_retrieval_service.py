import logging

from allauth.socialaccount.models import SocialToken
from django.utils.translation import gettext as _
from injector import inject

from main.apps.api_auth.services import SocialAccountRetrievalService
from main.apps.core.exceptions import NotFoundError
from main.apps.users.models import User


logger = logging.getLogger(__name__)


class SocialTokenRetrievalService:
    @inject
    def __init__(self, social_account_retrieval_service: SocialAccountRetrievalService):
        self._social_account_retrieval_service = social_account_retrieval_service

    def get_social_token_detail(self, user: User, provider: str) -> SocialToken:
        social_account = self._social_account_retrieval_service.get_social_account_detail(user, provider)
        try:
            return SocialToken.objects.filter(account=social_account).get()
        except SocialToken.DoesNotExist:
            logger.warning(f"Social token not found for user: {user.id} and provider: {provider}")
            raise NotFoundError(_("Social token not found"))
