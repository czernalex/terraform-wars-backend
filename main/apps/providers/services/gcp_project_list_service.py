import logging
from typing import Iterable, override

from allauth.socialaccount.models import SocialApp, SocialToken
from django.conf import settings
from django.utils.translation import gettext as _
from injector import inject
from ninja.errors import ValidationError

from main.apps.api_auth.services import SocialAppRetrievalService, SocialTokenRetrievalService
from main.apps.gcp.services import GCPOAuth2CredentialsCreateService, GCPProjectSearchService
from main.apps.providers.models import ProviderUserProject
from main.apps.providers.schemas import ProviderProjectSchema
from main.apps.providers.services.provider_project_list_service import ProviderProjectListService
from main.apps.providers.services.provider_user_project_retrieval_service import ProviderUserProjectRetrievalService


logger = logging.getLogger(__name__)


class GCPProjectListService(ProviderProjectListService):
    @inject
    def __init__(
        self,
        social_app_retrieval_service: SocialAppRetrievalService,
        social_token_retrieval_service: SocialTokenRetrievalService,
        provider_user_project_retrieval_service: ProviderUserProjectRetrievalService,
        gcp_oauth2_credentials_create_service: GCPOAuth2CredentialsCreateService,
        gcp_project_search_service: GCPProjectSearchService,
    ):
        super().__init__(
            social_app_retrieval_service, social_token_retrieval_service, provider_user_project_retrieval_service
        )
        self._gcp_oauth2_credentials_create_service = gcp_oauth2_credentials_create_service
        self._gcp_project_search_service = gcp_project_search_service

    def _get_credentials_scope(self) -> list[str]:
        return settings.SOCIALACCOUNT_PROVIDERS["google"]["SCOPE"]

    @override
    def get_provider_id(self) -> str:
        return "google"

    @override
    def _list_projects(
        self, social_app: SocialApp, social_token: SocialToken, provider_user_projects: Iterable[ProviderUserProject]
    ) -> list[ProviderProjectSchema]:
        credentials = self._gcp_oauth2_credentials_create_service.create(
            social_token.token_secret,
            social_app.client_id,
            social_app.secret,
            self._get_credentials_scope(),
        )
        try:
            return list(
                ProviderProjectSchema(
                    project_id=project.project_id,
                    project_number=project.name,
                    display_name=project.display_name,
                    parent_name=project.parent,
                    is_linked_with_provider_user_project=any(
                        provider_user_project.project_id == project.project_id
                        for provider_user_project in provider_user_projects
                    ),
                )
                for project in self._gcp_project_search_service.search(credentials)
            )
        except Exception as error:
            logger.error("Error occured while trying to search GCP projects, error: %s", str(error))
            raise ValidationError(
                [
                    {
                        "loc": ["projects"],
                        "msg": _(
                            "Error occured while trying to list GCP projects. If error persists, try revoking access to Terraform Wars OAuth app and reconnect your google account with Terraform Wars."
                        ),
                        "type": "value_error",
                    }
                ]
            )
