from main.apps.users.models.user import User


class TestUser:
    def test_full_name(self):
        user = User(first_name="John", last_name="Doe", username="john.doe", email="john.doe@example.com")
        assert user.full_name == "John Doe"

    def test_full_name_username(self):
        user = User(first_name="John", username="john.doe", email="john.doe@example.com")
        assert user.full_name == "john.doe"

    def test_full_name_email(self):
        user = User(email="john.doe@example.com")
        assert user.full_name == "john.doe@example.com"

    def test_str(self):
        user = User(first_name="John", last_name="Doe", username="john.doe", email="john.doe@example.com")
        assert str(user) == "John Doe"
