import logging
from uuid import UUID

from allauth.account.models import EmailAddress
from django.db import transaction
from injector import inject

from main.apps.users.models import User
from main.apps.users.services.user_retrieval_service import UserRetrievalService


logger = logging.getLogger(__name__)


class UserDeleteService:
    @inject
    def __init__(self, user_retrieval_service: UserRetrievalService):
        self._user_retrieval_service = user_retrieval_service

    def _delete_user_email_addresses(self, user: User) -> None:
        # FIXME: Breaks SRP, move to a separate service
        EmailAddress.objects.filter(user=user).delete()

    def _anonymize_user(self, user: User) -> User:
        user.email = f"deleted_{user.id}@none"
        user.username = ""
        user.first_name = ""
        user.last_name = ""
        user.last_login = None
        user.is_staff = False
        user.is_superuser = False
        return user

    def _deactivate_user(self, user: User) -> User:
        user.is_active = False
        user.set_unusable_password()
        return user

    @transaction.atomic
    def delete(self, user_id: UUID) -> None:
        logger.info(f"Deleting user: {user_id}")
        user = self._user_retrieval_service.get_for_update_by_id(user_id)
        user = self._anonymize_user(user)
        user = self._deactivate_user(user)
        user.save()
        self._delete_user_email_addresses(user)
        logger.info(f"User: {user_id} deleted and anonymized successfully")
