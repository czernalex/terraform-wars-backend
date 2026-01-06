from typing import Optional
from uuid import UUID

from django.utils.translation import gettext as _

from main.apps.users.models import User


class UserValidationService:
    def validate_username(self, username: Optional[str], user_id: Optional[UUID] = None) -> None:
        if not username:
            return

        if User.objects.for_username(username).exclude(id=user_id).exists():
            raise ValueError(_("Username is already taken"))
