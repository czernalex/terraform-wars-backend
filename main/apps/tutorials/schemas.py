from typing import Annotated, Optional
from uuid import UUID

from django.db.models import Q
from ninja import Field, FilterLookup, FilterSchema, ModelSchema, Schema

from main.apps.providers.schemas import ProviderSchema
from main.apps.tutorials.enums import Difficulty, TutorialStatus
from main.apps.tutorials.models import (
    Tutorial,
    TutorialSubmission,
    TutorialTag,
)


class TutorialTagListFilterSchema(FilterSchema):
    ids: Annotated[Optional[list[UUID]], FilterLookup(["id__in"])] = None
    search: Annotated[Optional[str], FilterLookup(["name__icontains"])] = None


class TutorialTagSchema(ModelSchema):
    id: UUID

    class Meta:
        model = TutorialTag
        fields = [
            "name",
            "slug",
        ]


class TutorialListFilterSchema(FilterSchema):
    search: Annotated[
        Optional[str], FilterLookup(["title__icontains", "description__icontains", "provider__name__icontains"])
    ] = None
    slug: Optional[str] = None
    status: Optional[TutorialStatus] = None
    difficulty: Optional[Difficulty] = None
    provider_id: Optional[UUID] = None
    tag_ids: Annotated[Optional[list[UUID]], FilterLookup(["tags__id__in"])] = None
    author_id: Optional[UUID] = None
    exclude_id: Optional[UUID] = None

    def filter_exclude_id(self, value: UUID) -> Q:
        return ~Q(id=value)


class TutorialListSchema(ModelSchema):
    id: UUID
    provider: ProviderSchema
    author_email: Optional[str]
    author_username: Optional[str]
    tags: list[TutorialTagSchema]
    difficulty: Difficulty
    status: TutorialStatus

    class Meta:
        model = Tutorial
        fields = [
            "title",
            "slug",
            "description",
            "created_at",
            "updated_at",
        ]

    @staticmethod
    def resolve_author_email(obj: Tutorial) -> Optional[str]:
        return obj.author.email if obj.author else None

    @staticmethod
    def resolve_author_username(obj: Tutorial) -> Optional[str]:
        return obj.author.username if obj.author else None


class CreateTutorialSchema(Schema):
    provider_id: UUID
    title: str = Field(..., min_length=1, max_length=255)
    description: str
    assignment: str
    difficulty: Difficulty
    tag_ids: list[UUID]
    validation_script: str
    code_template: str
    status: TutorialStatus


class UpdateTutorialSchema(Schema):
    provider_id: UUID
    title: str = Field(..., min_length=1, max_length=255)
    description: str
    assignment: str
    difficulty: Difficulty
    tag_ids: list[UUID]
    validation_script: str
    code_template: str
    status: TutorialStatus


class PartialUpdateTutorialSchema(Schema):
    status: Optional[TutorialStatus] = None


class TutorialDetailSchema(ModelSchema):
    id: UUID
    provider: ProviderSchema
    author_email: Optional[str]
    author_username: Optional[str]
    tags: list[TutorialTagSchema]
    difficulty: Difficulty
    status: TutorialStatus
    validation_script: str
    code_template: str

    class Meta:
        model = Tutorial
        fields = [
            "title",
            "slug",
            "description",
            "assignment",
            "config_data",
            "created_at",
            "updated_at",
        ]

    @staticmethod
    def resolve_author_email(obj: Tutorial) -> Optional[str]:
        return obj.author.email if obj.author else None

    @staticmethod
    def resolve_author_username(obj: Tutorial) -> Optional[str]:
        return obj.author.username if obj.author else None


class CreateTutorialSubmissionSchema(Schema):
    tutorial_id: UUID
    provider_user_project_id: UUID
    code: str


class UpdateTutorialSubmissionSchema(Schema):
    code: str


class TutorialSubmissionDetailSchema(ModelSchema):
    id: UUID

    class Meta:
        model = TutorialSubmission
        fields = [
            "code",
        ]
