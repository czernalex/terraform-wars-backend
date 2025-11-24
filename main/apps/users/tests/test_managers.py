import pytest
from model_bakery import baker

from main.apps.users.models import User


@pytest.mark.django_db(transaction=True)
class TestUserQuerySet:
    def test_is_active(self):
        baker.make_recipe("main.apps.users.tests.active_user")
        baker.make_recipe("main.apps.users.tests.inactive_user")

        users = User.objects.is_active(True)

        assert users.count() == 1
        assert users.first().is_active is True

    def test_for_email(self):
        baker.make_recipe("main.apps.users.tests.active_user", email="test@example.com")
        baker.make_recipe("main.apps.users.tests.active_user", email="test2@example.com")

        users = list(User.objects.for_email("test@example.com"))

        assert len(users) == 1
        assert users[0].email == "test@example.com"

    def test_for_username(self):
        baker.make_recipe("main.apps.users.tests.active_user", username="test")
        baker.make_recipe("main.apps.users.tests.active_user", username="test2")

        users = list(User.objects.for_username("test"))

        assert len(users) == 1
        assert users[0].username == "test"

    def test_search(self):
        baker.make_recipe(
            "main.apps.users.tests.active_user",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            username="john.doe",
        )
        baker.make_recipe("main.apps.users.tests.inactive_user", email="test2@example.com")

        users = list(User.objects.search("john doe"))

        assert len(users) == 1
        assert users[0].email == "test@example.com"
        assert users[0].first_name == "John"
        assert users[0].last_name == "Doe"
        assert users[0].username == "john.doe"


@pytest.mark.django_db(transaction=True)
class TestUserManager:
    def test_get_queryset(self):
        baker.make_recipe("main.apps.users.tests.active_user")
        baker.make_recipe("main.apps.users.tests.inactive_user")
        assert User.all_objects.count() == 2


@pytest.mark.django_db(transaction=True)
class TestActiveUserManager:
    def test_get_queryset(self):
        baker.make_recipe("main.apps.users.tests.active_user")
        baker.make_recipe("main.apps.users.tests.inactive_user")
        assert User.objects.count() == 1
