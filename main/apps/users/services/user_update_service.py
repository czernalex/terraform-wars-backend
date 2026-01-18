import logging
from uuid import UUID

from django.db import transaction
from injector import inject

from main.apps.users.models import User
from main.apps.users.schemas import UserUpdateSchema
from main.apps.users.services.user_retrieval_service import UserRetrievalService
from main.apps.users.services.user_validation_service import UserValidationService

logger = logging.getLogger(__name__)


class UserUpdateService:
    @inject
    def __init__(
        self,
        user_retrieval_service: UserRetrievalService,
        user_validation_service: UserValidationService,
    ):
        self._user_retrieval_service = user_retrieval_service
        self._user_validation_service = user_validation_service

    def _validate_data(self, user_id: UUID, data: UserUpdateSchema) -> None:
        self._user_validation_service.validate_username(data.username, user_id)

    def _update_user_with_data(self, user: User, data: UserUpdateSchema) -> User:
        user.username = data.username or ""
        user.first_name = data.first_name or ""
        user.last_name = data.last_name or ""
        user.save()
        return user

    @transaction.atomic
    def update(self, user_id: UUID, data: UserUpdateSchema) -> User:
        logger.info(f"Updating user: {user_id}, data: {data}")
        user = self._user_retrieval_service.get_for_update_by_id(user_id)
        self._validate_data(user_id, data)
        user = self._update_user_with_data(user, data)
        logger.info(f"User: {user_id} updated successfully")
        return user
