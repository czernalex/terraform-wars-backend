from typing import Optional
from uuid import UUID

from django.utils.translation import gettext as _
from injector import inject
from ninja.errors import ValidationError

from main.apps.users.services.user_retrieval_service import UserRetrievalService


class UserValidationService:
    @inject
    def __init__(self, user_retrieval_service: UserRetrievalService):
        self._user_retrieval_service = user_retrieval_service

    def validate_username(self, username: Optional[str], user_id: Optional[UUID] = None) -> None:
        if not username:
            return

        if self._user_retrieval_service.try_find_by_username(username, user_id):
            raise ValidationError(
                [
                    {
                        "loc": ["username"],
                        "msg": _("Username is already taken"),
                        "type": "value_error",
                    }
                ]
            )
