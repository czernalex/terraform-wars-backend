from uuid import UUID

from django.db import transaction

from main.apps.users.models.user import User


class UserRetrievalService:
    def get_for_read_by_id(self, user_id: UUID) -> User:
        return User.objects.get(id=user_id)

    @transaction.atomic
    def get_for_update_by_id(self, user_id: UUID) -> User:
        return User.objects.select_for_update(of=("self",)).get(id=user_id)
