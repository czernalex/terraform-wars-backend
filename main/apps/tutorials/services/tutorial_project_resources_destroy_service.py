import logging
from abc import ABC, abstractmethod
from typing import override

from allauth.socialaccount.models import SocialApp, SocialToken
from injector import inject
from django.conf import settings
from django.utils.translation import gettext as _

from main.apps.api_auth.services import SocialAppRetrievalService, SocialTokenRetrievalService
from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.models import TutorialProject
from main.apps.tutorials.services.gcp_credentials_service import GCPCredentialsService
from main.apps.tutorials.services.gcp_project_delete_service import GCPProjectDeleteService


logger = logging.getLogger(__name__)


class TutorialProjectResourcesDestroyService(ABC):
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
            return self._social_app_retrieval_service.get_social_app_detail(self.get_provider_id())
        except NotFoundError as error:
            raise ValueError(_("Social app not found")) from error

    def _get_social_token(self, tutorial_project: TutorialProject) -> SocialToken:
        try:
            return self._social_token_retrieval_service.get_social_token_detail(
                tutorial_project.user, self.get_provider_id()
            )
        except NotFoundError as error:
            raise ValueError(_("Social token not found")) from error

    @abstractmethod
    def get_provider_id(self) -> str:
        pass

    @abstractmethod
    def destroy(self, tutorial_project: TutorialProject) -> None:
        pass


class GCPTutorialProjectResourcesDestroyService(TutorialProjectResourcesDestroyService):
    @inject
    def __init__(
        self,
        social_app_retrieval_service: SocialAppRetrievalService,
        social_token_retrieval_service: SocialTokenRetrievalService,
        gcp_credentials_service: GCPCredentialsService,
        gcp_project_delete_service: GCPProjectDeleteService,
    ):
        super().__init__(social_app_retrieval_service, social_token_retrieval_service)
        self._gcp_credentials_service = gcp_credentials_service
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
        credentials = self._gcp_credentials_service.get_credentials(
            social_token, social_app, settings.SOCIALACCOUNT_PROVIDERS[self.get_provider_id()]["SCOPE"]
        )
        logger.info(f"Destroying GCP project: {tutorial_project.config_data['gcp_project_id']}")
        self._gcp_project_delete_service.delete(credentials, tutorial_project.config_data["gcp_project_name"])
        logger.info(f"GCP project: {tutorial_project.config_data['gcp_project_id']} destroyed successfully")
