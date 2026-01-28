import logging
from typing import Optional
from uuid import UUID

from django.utils.text import slugify
from django.utils.translation import gettext as _
from injector import inject
from ninja.errors import ValidationError

from main.apps.core.exceptions import NotFoundError
from main.apps.providers.models import Provider
from main.apps.providers.services.provider_retrieval_service import ProviderRetrievalService
from main.apps.tutorials.enums import TutorialStatus
from main.apps.tutorials.models import Tutorial, TutorialTag
from main.apps.tutorials.schemas import (
    CreateTutorialSchema,
    PartialUpdateTutorialSchema,
    TutorialListFilterSchema,
    TutorialTagListFilterSchema,
    UpdateTutorialSchema,
)
from main.apps.tutorials.services.tutorial_retrieval_service import TutorialRetrievalService
from main.apps.tutorials.services.tutorial_tag_retrieval_service import TutorialTagRetrievalService
from main.apps.tutorials.types import CreateOrUpdateTutorialValidatedData


logger = logging.getLogger(__name__)


class TutorialValidationService:
    @inject
    def __init__(
        self,
        tutorial_retrieval_service: TutorialRetrievalService,
        provider_retrieval_service: ProviderRetrievalService,
        tutorial_tag_retrieval_service: TutorialTagRetrievalService,
    ):
        self._tutorial_retrieval_service = tutorial_retrieval_service
        self._provider_retrieval_service = provider_retrieval_service
        self._tutorial_tag_retrieval_service = tutorial_tag_retrieval_service

    def _validate_provider_exists(self, provider_id: UUID) -> Provider:
        try:
            return self._provider_retrieval_service.get_detail_by_id(provider_id)
        except NotFoundError as error:
            logger.warning("Provider not found: %(provider_id)s", {"provider_id": provider_id})
            raise ValidationError(
                [
                    {
                        "loc": ["provider_id"],
                        "msg": str(error),
                        "type": "value_error",
                    }
                ]
            ) from error

    def _validate_tags_exist(self, tag_ids: list[UUID]) -> list[TutorialTag]:
        existing_tag_ids = list(
            self._tutorial_tag_retrieval_service.get_list(filters=TutorialTagListFilterSchema(ids=tag_ids)).values_list(
                "id", flat=True
            )
        )
        for tag_id in tag_ids:
            if tag_id not in existing_tag_ids:
                raise ValidationError(
                    [
                        {
                            "loc": ["tag_ids"],
                            "msg": _("Tag with id %(tag_id)s not found") % {"tag_id": tag_id},
                            "type": "value_error",
                        }
                    ]
                )
        return existing_tag_ids

    def _validate_unique_slug(self, slug: str, tutorial_id: Optional[UUID] = None) -> None:
        if self._tutorial_retrieval_service.get_list(
            filters=TutorialListFilterSchema(slug=slug, exclude_id=tutorial_id)
        ):
            raise ValidationError(
                [
                    {
                        "loc": ["slug"],
                        "msg": _("Slug is not unique"),
                        "type": "value_error",
                    }
                ]
            )

    def _validate_post_status(self, status: TutorialStatus) -> None:
        if status not in [TutorialStatus.DRAFT, TutorialStatus.REVIEW]:
            raise ValidationError(
                [
                    {
                        "loc": ["status"],
                        "msg": _("Status must be draft or review"),
                        "type": "value_error",
                    }
                ]
            )

    def _validate_pre_update_status(self, status: TutorialStatus) -> None:
        if status not in [TutorialStatus.DRAFT, TutorialStatus.REJECTED]:
            raise ValidationError(
                [
                    {
                        "loc": ["status"],
                        "msg": _("To update the tutorial, the status must be draft or rejected"),
                        "type": "value_error",
                    }
                ]
            )

    def validate_create_data(self, data: CreateTutorialSchema) -> CreateOrUpdateTutorialValidatedData:
        slug = slugify(data.title)
        self._validate_unique_slug(slug)
        self._validate_post_status(data.status)
        provider = self._validate_provider_exists(data.provider_id)
        tag_ids = self._validate_tags_exist(data.tag_ids)
        return CreateOrUpdateTutorialValidatedData(
            provider=provider,
            slug=slug,
            status=data.status,
            tag_ids=tag_ids,
        )

    def validate_update_data(
        self, tutorial: Tutorial, data: UpdateTutorialSchema
    ) -> CreateOrUpdateTutorialValidatedData:
        slug = slugify(data.title)
        self._validate_unique_slug(slug, tutorial.id)
        self._validate_pre_update_status(tutorial.status)
        self._validate_post_status(data.status)
        provider = self._validate_provider_exists(data.provider_id)
        tag_ids = self._validate_tags_exist(data.tag_ids)
        return CreateOrUpdateTutorialValidatedData(
            provider=provider,
            slug=slug,
            status=data.status,
            tag_ids=tag_ids,
        )

    def validate_partial_update_data(self, tutorial: Tutorial, data: PartialUpdateTutorialSchema) -> None:
        # TODO: Validate the status flow
        return

    def validate_accepts_submissions(self, tutorial: Tutorial, loc: str = "tutorial_id") -> None:
        if tutorial.status != TutorialStatus.PUBLISHED:
            error_message = f"Tutorial {tutorial.id} does not accept submissions"
            logger.warning(error_message)
            raise ValidationError(
                [
                    {
                        "loc": [loc],
                        "msg": error_message,
                        "type": "value_error",
                    }
                ]
            )

    def validate_can_be_deleted(self, tutorial: Tutorial) -> None:
        if tutorial.status not in [
            TutorialStatus.DRAFT,
            TutorialStatus.REVIEW,
            TutorialStatus.REJECTED,
            TutorialStatus.APPROVED,
        ]:
            raise ValidationError(
                [
                    {
                        "loc": ["status"],
                        "msg": _("Tutorial with status %(status)s cannot be deleted") % {"status": tutorial.status},
                        "type": "value_error",
                    }
                ]
            )
