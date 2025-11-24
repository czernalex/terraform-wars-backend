from typing import Optional
from uuid import UUID
from ninja import Field, ModelSchema, Schema

from main.apps.tutorials.enums import Difficulty
from main.apps.tutorials.models import Provider, Tutorial, TutorialTag


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


class TutorialListSchema(ModelSchema):
    id: UUID
    provider_id: UUID
    provider_name: str = Field(alias="provider.name")
    author_email: Optional[str] = Field(alias="author.email")
    author_username: Optional[str] = Field(alias="author.username")
    tags: list[TutorialTagSchema]
    difficulty: Difficulty

    class Meta:
        model = Tutorial
        fields = [
            "title",
            "slug",
            "created_at",
            "updated_at",
        ]


class TutorialDetailSchema(ModelSchema):
    id: UUID
    provider: ProviderSchema
    author_email: Optional[str] = Field(alias="author.email")
    author_username: Optional[str] = Field(alias="author.username")
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


class TutorialCreateSchema(Schema):
    title: str = Field(..., max_length=255)
    description: str


class TutorialUpdateSchema(TutorialCreateSchema):
    pass
