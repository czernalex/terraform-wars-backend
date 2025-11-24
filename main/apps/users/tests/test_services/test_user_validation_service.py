import pytest
from model_bakery import baker

from main.apps.users.services.user_validation_service import UserValidationService


@pytest.mark.django_db(transaction=True)
class TestUserValidationService:
    def test_validate_username_already_taken(self):
        baker.make_recipe("main.apps.users.tests.active_user", username="test")
        with pytest.raises(ValueError):
            UserValidationService().validate_username("test")

    def test_validate_username_update(self):
        user = baker.make_recipe("main.apps.users.tests.active_user", username="test")
        assert UserValidationService().validate_username("test", user_id=user.id) is None

    def test_validate_username_empty(self):
        baker.make_recipe("main.apps.users.tests.active_user", username="test")
        assert UserValidationService().validate_username("") is None
        assert UserValidationService().validate_username(None) is None
