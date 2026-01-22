import pytest
from model_bakery import baker

from main.di import injector
from main.apps.api_auth.services.social_account_retrieval_service import SocialAccountRetrievalService
from main.apps.core.exceptions import NotFoundError


@pytest.mark.django_db()
class TestSocialAccountRetrievalService:
    def test_get_social_account(self):
        social_account = baker.make_recipe("main.apps.api_auth.tests.social_account_google")
        service = injector.get(SocialAccountRetrievalService)
        assert (
            service.get_detail_by_user_id_and_provider(social_account.user.id, social_account.provider)
            == social_account
        )

    def test_get_social_account_not_found(self):
        user = baker.make_recipe("main.apps.users.tests.active_user")
        service = injector.get(SocialAccountRetrievalService)
        with pytest.raises(NotFoundError):
            service.get_detail_by_user_id_and_provider(user, "not_found")
