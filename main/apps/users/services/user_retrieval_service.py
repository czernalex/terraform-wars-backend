from uuid import UUID

from anydi import singleton

from main.apps.users.models.user import User


@singleton
class UserRetrievalService:
    def get_user_for_read(self, user_id: UUID) -> User:
        return User.objects.get(id=user_id)

    def get_user_for_update(self, user_id: UUID) -> User:
        return User.objects.select_for_update(of=("self",)).get(id=user_id)
