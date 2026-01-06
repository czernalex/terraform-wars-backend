from uuid import UUID

from django.db import transaction

from main.apps.users.models.user import User


class UserRetrievalService:
    def get_user_for_read(self, user_id: UUID) -> User:
        return User.objects.get(id=user_id)

    @transaction.atomic
    def get_user_for_update(self, user_id: UUID) -> User:
        return User.objects.select_for_update(of=("self",)).get(id=user_id)
