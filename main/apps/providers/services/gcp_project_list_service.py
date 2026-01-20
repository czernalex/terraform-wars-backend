import logging
from typing import override
from uuid import UUID

from allauth.socialaccount.models import SocialApp, SocialToken
from django.conf import settings
from django.utils.translation import gettext as _
from injector import inject
from ninja.errors import ValidationError

from main.apps.api_auth.services import SocialAppRetrievalService, SocialTokenRetrievalService
from main.apps.core.exceptions import NotFoundError
from main.apps.gcp.services import GCPOAuth2CredentialsCreateService, GCPProjectSearchService
from main.apps.providers.schemas import ProviderProjectSchema


logger = logging.getLogger(__name__)


class GCPProjectListService:
    @inject
    def __init__(
        self,
        social_app_retrieval_service: SocialAppRetrievalService,
        social_token_retrieval_service: SocialTokenRetrievalService,
        gcp_oauth2_credentials_create_service: GCPOAuth2CredentialsCreateService,
        gcp_project_search_service: GCPProjectSearchService,
    ):
        self._social_app_retrieval_service = social_app_retrieval_service
        self._social_token_retrieval_service = social_token_retrieval_service
        self._gcp_oauth2_credentials_create_service = gcp_oauth2_credentials_create_service
        self._gcp_project_search_service = gcp_project_search_service

    def _get_social_app(self) -> SocialApp:
        try:
            return self._social_app_retrieval_service.get_detail_by_provider("google")
        except NotFoundError as error:
            logger.error("Social app not found for google provider")
            raise ValidationError(
                [
                    {
                        "loc": ["social_app"],
                        "msg": _("Social app not found"),
                        "type": "value_error",
                    }
                ]
            )

    def _get_social_token(self, user_id: UUID) -> SocialToken:
        try:
            social_token = self._social_token_retrieval_service.get_detail_by_user_id_and_provider(user_id, "google")
        except NotFoundError as error:
            logger.warning("Social token not found for user: %s and provider: google", user_id)
            raise ValidationError(
                [
                    {
                        "loc": ["social_token"],
                        "msg": _("Social token not found"),
                        "type": "value_error",
                    }
                ]
            )

        if not social_token.token_secret:
            logger.error("Social token refresh token is missing for user: %s and provider: google", user_id)
            raise ValidationError(
                [
                    {
                        "loc": ["social_token"],
                        "msg": _("Social token refresh token is missing"),
                        "type": "value_error",
                    }
                ]
            )

        return social_token

    def _get_credentials_scope(self) -> list[str]:
        return settings.SOCIALACCOUNT_PROVIDERS["google"]["SCOPE"]

    @override
    def get_list(self, user_id: UUID) -> list[ProviderProjectSchema]:
        social_app = self._get_social_app()
        social_token = self._get_social_token(user_id)
        credentials = self._gcp_oauth2_credentials_create_service.create(
            social_token.token_secret,
            social_app.client_id,
            social_app.secret,
            self._get_credentials_scope(),
        )
        return list(
            ProviderProjectSchema(
                project_id=project.project_id,
                project_name=project.name,
                display_name=project.display_name,
                parent_name=project.parent,
            )
            for project in self._gcp_project_search_service.search(credentials)
        )
