import pytest

from main.di import injector
from main.apps.api_auth.services.social_app_retrieval_service import SocialAppRetrievalService
from main.apps.core.exceptions import NotFoundError
from model_bakery import baker


@pytest.mark.django_db()
class TestSocialAppRetrievalService:
    def test_get_social_app(self):
        social_app = baker.make_recipe("main.apps.api_auth.tests.social_app_google")
        service = injector.get(SocialAppRetrievalService)
        assert service.get_detail(social_app.provider) == social_app

    def test_get_social_app_not_found(self):
        service = injector.get(SocialAppRetrievalService)
        with pytest.raises(NotFoundError):
            service.get_detail("not_found")
