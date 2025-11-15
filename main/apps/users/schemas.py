from uuid import UUID

from ninja import ModelSchema

from main.apps.users.models import User


class UserDetailSchema(ModelSchema):
    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    full_name: str
    permissions: list[str]

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
        ]

    @staticmethod
    def resolve_permissions(obj: User) -> list[str]:
        return list(obj.get_all_permissions())
