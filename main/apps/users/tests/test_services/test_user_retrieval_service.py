import pytest
from model_bakery import baker

from main.di import injector
from main.apps.users.services.user_retrieval_service import UserRetrievalService


@pytest.mark.django_db()
class TestUserRetrievalService:
    def test_get_user_for_read(self):
        user = baker.make_recipe("main.apps.users.tests.active_user")
        service = injector.get(UserRetrievalService)
        assert service.get_for_read_by_id(user.id) == user

    def test_get_user_for_update(self):
        user = baker.make_recipe("main.apps.users.tests.active_user")
        service = injector.get(UserRetrievalService)
        assert service.get_for_update_by_id(user.id) == user
