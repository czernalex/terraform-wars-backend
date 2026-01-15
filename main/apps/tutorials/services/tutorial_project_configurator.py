import logging
from abc import ABC, abstractmethod

from allauth.socialaccount.models import SocialApp, SocialToken
from injector import inject
from django.utils.translation import gettext as _

from main.apps.api_auth.services import SocialAppRetrievalService, SocialTokenRetrievalService
from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.models import TutorialProject


logger = logging.getLogger(__name__)


class TutorialProjectConfigurator(ABC):
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
            return self._social_app_retrieval_service.get_detail(self.get_provider_id())
        except NotFoundError as error:
            raise ValueError(_("Social app not found")) from error

    def _get_social_token(self, tutorial_project: TutorialProject) -> SocialToken:
        try:
            return self._social_token_retrieval_service.get_detail(tutorial_project.user, self.get_provider_id())
        except NotFoundError as error:
            raise ValueError(_("Social token not found")) from error

    @abstractmethod
    def get_provider_id(self) -> str:
        pass

    @abstractmethod
    def configure(self, tutorial_project: TutorialProject) -> None:
        # Supported terraform providers will implement this method to setup environment for the tutorial
        pass
