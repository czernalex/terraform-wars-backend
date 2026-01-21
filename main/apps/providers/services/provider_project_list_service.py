import logging
from abc import ABC, abstractmethod
from uuid import UUID

from allauth.socialaccount.models import SocialApp, SocialToken
from django.utils.translation import gettext as _
from injector import inject
from ninja.errors import ValidationError

from main.apps.api_auth.services import SocialAppRetrievalService, SocialTokenRetrievalService
from main.apps.core.exceptions import NotFoundError
from main.apps.providers.models import Provider
from main.apps.providers.schemas import ProviderProjectSchema


logger = logging.getLogger(__name__)


class ProviderProjectListService(ABC):
    @inject
    def __init__(
        self,
        social_app_retrieval_service: SocialAppRetrievalService,
        social_token_retrieval_service: SocialTokenRetrievalService,
    ):
        self._social_app_retrieval_service = social_app_retrieval_service
        self._social_token_retrieval_service = social_token_retrieval_service

    def _get_social_app(self) -> SocialApp:
        try:
            return self._social_app_retrieval_service.get_detail_by_provider(self.get_provider_id())
        except NotFoundError as error:
            logger.error("Social app not found for provider: %s", self.get_provider_id())
            raise ValidationError(
                [
                    {
                        "loc": ["social_app"],
                        "msg": _("Provider is not supported"),
                        "type": "value_error",
                    }
                ]
            )

    def _get_social_token(self, user_id: UUID) -> SocialToken:
        try:
            social_token = self._social_token_retrieval_service.get_detail_by_user_id_and_provider(
                user_id, self.get_provider_id()
            )
        except NotFoundError as error:
            logger.warning("Social token not found for user: %s and provider: %s", user_id, self.get_provider_id())
            raise ValidationError(
                [
                    {
                        "loc": ["social_token"],
                        "msg": _("Your account is not linked to %(provider)s") % {"provider": self.get_provider_id()},
                        "type": "value_error",
                    }
                ]
            )

        if not social_token.token_secret:
            logger.error(
                "Social token refresh token is missing for user: %s and provider: %s", user_id, self.get_provider_id()
            )
            raise ValidationError(
                [
                    {
                        "loc": ["social_token"],
                        "msg": _(
                            "Your account is not correctly linked to %(provider)s. Try revoking access to Terraform Wars OAuth app and reconnecting."
                        )
                        % {"provider": self.get_provider_id()},
                        "type": "value_error",
                    }
                ]
            )

        return social_token

    @abstractmethod
    def get_provider_id(self) -> str:
        pass

    @abstractmethod
    def _list_projects(self) -> list[ProviderProjectSchema]:
        pass

    def get_list(self, user_id: UUID, provider: Provider) -> list[ProviderProjectSchema]:
        social_app = self._get_social_app()
        social_token = self._get_social_token(user_id)
        return self._list_projects(social_app, social_token)
