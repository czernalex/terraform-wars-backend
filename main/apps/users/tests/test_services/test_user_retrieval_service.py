import uuid
import pytest
from model_bakery import baker

from main.apps.core.exceptions import NotFoundError
from main.di import injector
from main.apps.users.services.user_retrieval_service import UserRetrievalService


@pytest.mark.django_db()
class TestUserRetrievalService:
    def test_get_user_for_read(self):
        user = baker.make_recipe("main.apps.users.tests.active_user")
        service = injector.get(UserRetrievalService)
        assert service.get_detail_by_id(user.id) == user

    def test_get_user_not_found(self):
        service = injector.get(UserRetrievalService)
        with pytest.raises(NotFoundError):
            service.get_detail_by_id(uuid.uuid7())

    def test_get_user_for_update(self):
        user = baker.make_recipe("main.apps.users.tests.active_user")
        service = injector.get(UserRetrievalService)
        assert service.get_for_update_by_id(user.id) == user

    def test_get_user_for_update_not_found(self):
        service = injector.get(UserRetrievalService)
        with pytest.raises(NotFoundError):
            service.get_for_update_by_id(uuid.uuid7())

    def test_find_by_username(self):
        user = baker.make_recipe("main.apps.users.tests.active_user", username="test")
        service = injector.get(UserRetrievalService)
        assert service.try_find_by_username("test") == user

    def test_find_by_username_not_found(self):
        service = injector.get(UserRetrievalService)
        assert service.try_find_by_username("test") is None
