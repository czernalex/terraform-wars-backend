from typing import Optional
from uuid import UUID

from ninja import Field, ModelSchema, Schema

from main.apps.users.models import User


class UserDetailSchema(ModelSchema):
    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    full_name: str
    permissions: list[str]
    is_staff: bool
    has_usable_password: bool

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
        ]

    @staticmethod
    def resolve_permissions(obj: User) -> list[str]:
        return list(obj.get_all_permissions())


class UserUpdateSchema(Schema):
    username: Optional[str] = Field(..., max_length=255)
    first_name: Optional[str] = Field(..., max_length=255)
    last_name: Optional[str] = Field(..., max_length=255)
