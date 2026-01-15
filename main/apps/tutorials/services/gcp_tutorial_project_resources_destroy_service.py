import logging
from typing import override

from allauth.socialaccount.models import SocialToken
from injector import inject
from django.conf import settings
from django.utils.translation import gettext as _

from main.apps.api_auth.services import SocialAppRetrievalService, SocialTokenRetrievalService
from main.apps.gcp.services.gcp_credentials_create_service import GCPCredentialsCreateService
from main.apps.gcp.services.gcp_project_delete_service import GCPProjectDeleteService
from main.apps.tutorials.models import TutorialProject
from main.apps.tutorials.services.tutorial_project_resources_destroy_service import (
    TutorialProjectResourcesDestroyService,
)


logger = logging.getLogger(__name__)


class GCPTutorialProjectResourcesDestroyService(TutorialProjectResourcesDestroyService):
    @inject
    def __init__(
        self,
        social_app_retrieval_service: SocialAppRetrievalService,
        social_token_retrieval_service: SocialTokenRetrievalService,
        gcp_credentials_create_service: GCPCredentialsCreateService,
        gcp_project_delete_service: GCPProjectDeleteService,
    ):
        super().__init__(social_app_retrieval_service, social_token_retrieval_service)
        self._gcp_credentials_create_service = gcp_credentials_create_service
        self._gcp_project_delete_service = gcp_project_delete_service

    @override
    def _get_social_token(self, tutorial_project: TutorialProject) -> SocialToken:
        social_token = super()._get_social_token(tutorial_project)
        if not social_token.token_secret:
            raise ValueError(_("Refresh token is missing"))
        return social_token

    @override
    def get_provider_id(self) -> str:
        return "google"

    @override
    def destroy(self, tutorial_project: TutorialProject) -> None:
        social_token = self._get_social_token(tutorial_project)
        social_app = self._get_social_app()
        credentials = self._gcp_credentials_create_service.create(
            social_token, social_app, settings.SOCIALACCOUNT_PROVIDERS[self.get_provider_id()]["SCOPE"]
        )
        logger.info(f"Destroying GCP project: {tutorial_project.config_data['gcp_project_id']}")
        self._gcp_project_delete_service.delete(credentials, tutorial_project.config_data["gcp_project_name"])
        logger.info(f"GCP project: {tutorial_project.config_data['gcp_project_id']} destroyed successfully")
