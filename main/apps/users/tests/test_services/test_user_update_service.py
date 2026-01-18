from ninja.errors import ValidationError
import pytest
from model_bakery import baker

from main.di import injector
from main.apps.users.schemas import UserUpdateSchema
from main.apps.users.services.user_update_service import UserUpdateService


@pytest.mark.django_db()
class TestUserUpdateService:
    def test_update_user(self):
        user = baker.make_recipe("main.apps.users.tests.active_user")
        data = UserUpdateSchema(
            username="john.doe",
            first_name="John",
            last_name="Doe",
        )
        service = injector.get(UserUpdateService)
        updated_user = service.update(user.id, data)

        assert updated_user.username == data.username
        assert updated_user.first_name == data.first_name
        assert updated_user.last_name == data.last_name

    def test_update_user_with_occupied_username(self):
        user = baker.make_recipe("main.apps.users.tests.active_user")
        baker.make_recipe("main.apps.users.tests.active_user", username="john.doe")
        service = injector.get(UserUpdateService)
        with pytest.raises(ValidationError):
            service.update(user.id, UserUpdateSchema(username="john.doe", first_name="John", last_name="Doe"))
