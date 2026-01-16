from typing import Annotated, Optional
from uuid import UUID
from ninja import Field, FilterLookup, FilterSchema, ModelSchema, Schema

from main.apps.tutorials.enums import Difficulty, TutorialProjectStatus, TutorialStatus
from main.apps.tutorials.models import (
    Provider,
    Tutorial,
    TutorialProject,
    TutorialSubmission,
    TutorialTag,
)
from main.apps.users.schemas import UserDetailSchema


class ProviderSchema(ModelSchema):
    id: UUID

    class Meta:
        model = Provider
        fields = [
            "name",
            "slug",
            "description",
            "website_url",
            "created_at",
            "updated_at",
        ]


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
    status: Optional[TutorialStatus] = None
    difficulty: Optional[Difficulty] = None
    provider_id: Optional[UUID] = None
    tag_ids: Annotated[Optional[list[UUID]], FilterLookup(["tags__id__in"])] = None


class TutorialListSchema(ModelSchema):
    id: UUID
    provider_id: UUID
    provider_name: str = Field(alias="provider.name")
    author_email: Optional[str]
    author_username: Optional[str]
    tags: list[TutorialTagSchema]
    difficulty: Difficulty

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


class TutorialDetailSchema(ModelSchema):
    id: UUID
    provider: ProviderSchema
    author_email: Optional[str]
    author_username: Optional[str]
    tags: list[TutorialTagSchema]
    difficulty: Difficulty

    class Meta:
        model = Tutorial
        fields = [
            "title",
            "slug",
            "description",
            "assignment",
            "config_data",
            "code_template",
            "created_at",
            "updated_at",
        ]

    @staticmethod
    def resolve_author_email(obj: Tutorial) -> Optional[str]:
        return obj.author.email if obj.author else None

    @staticmethod
    def resolve_author_username(obj: Tutorial) -> Optional[str]:
        return obj.author.username if obj.author else None


class TutorialProjectListFilterSchema(FilterSchema):
    status: Optional[TutorialProjectStatus] = None
    provider_id: Optional[UUID] = None


class CreateTutorialProjectSchema(Schema):
    tutorial_id: UUID


class TutorialProjectListSchema(ModelSchema):
    id: UUID
    tutorial: TutorialDetailSchema
    user_id: UUID = Field(alias="user.id")
    status: TutorialProjectStatus

    class Meta:
        model = TutorialProject
        fields = [
            "config_data",
        ]


class TutorialProjectDetailSchema(ModelSchema):
    id: UUID
    tutorial: TutorialDetailSchema
    user: UserDetailSchema
    status: TutorialProjectStatus

    class Meta:
        model = TutorialProject
        fields = [
            "config_data",
        ]


class CreateTutorialSubmissionSchema(Schema):
    tutorial_id: UUID
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
