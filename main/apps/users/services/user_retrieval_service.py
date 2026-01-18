import logging
from typing import Optional
from uuid import UUID

from django.db import models, transaction
from django.utils.translation import gettext as _

from main.apps.core.exceptions import NotFoundError
from main.apps.users.models.user import User


logger = logging.getLogger(__name__)


class UserRetrievalService:
    def _get_queryset(self) -> models.QuerySet[User]:
        return User.objects.all()

    def _get_for_read_by_id(self, user_id: UUID) -> User:
        return self._get_queryset().get(id=user_id)

    def _get_for_update_by_id(self, user_id: UUID) -> User:
        return self._get_queryset().select_for_update(of=("self",)).get(id=user_id)

    def get_detail_by_id(self, user_id: UUID) -> User:
        try:
            return self._get_for_read_by_id(user_id)
        except User.DoesNotExist:
            raise NotFoundError(_("User not found"))

    @transaction.atomic
    def get_for_update_by_id(self, user_id: UUID) -> User:
        try:
            return self._get_for_update_by_id(user_id)
        except User.DoesNotExist:
            logger.warning(f"User: {user_id} not found")
            raise NotFoundError(_("User not found"))

    def find_by_username(self, username: str, exclude_user_id: Optional[UUID] = None) -> Optional[User]:
        qs = self._get_queryset().for_username(username)
        if exclude_user_id:
            qs = qs.exclude(id=exclude_user_id)
        return qs.first()
