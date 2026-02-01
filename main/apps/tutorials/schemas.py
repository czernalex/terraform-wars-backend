from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from django.db.models import Q
from ninja import Field, FilterLookup, FilterSchema, ModelSchema, Schema

from main.apps.providers.schemas import ProviderSchema
from main.apps.tutorials.enums import Difficulty, TutorialStatus, TutorialSubmissionStatus
from main.apps.tutorials.models import (
    Tutorial,
    TutorialSubmission,
    TutorialSubmissionEvent,
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
    is_completed_by_user: Optional[bool] = None

    def filter_exclude_id(self, value: UUID) -> Q:
        return ~Q(id=value)


class TutorialStatsSchema(Schema):
    upvote_count: int
    downvote_count: int
    completed_count: int
    submissions_count: int
    is_completed_by_user: bool


class TutorialListSchema(ModelSchema):
    id: UUID
    provider: ProviderSchema
    author_email: Optional[str]
    author_username: Optional[str]
    tags: list[TutorialTagSchema]
    difficulty: Difficulty
    status: TutorialStatus
    stats: TutorialStatsSchema

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

    @staticmethod
    def resolve_stats(obj: Tutorial) -> TutorialStatsSchema:
        return TutorialStatsSchema(
            upvote_count=obj.upvote_count,
            downvote_count=obj.downvote_count,
            completed_count=obj.completed_count,
            submissions_count=obj.submissions_count,
            is_completed_by_user=obj.is_completed_by_user,
        )


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
    stats: TutorialStatsSchema

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

    @staticmethod
    def resolve_stats(obj: Tutorial) -> TutorialStatsSchema:
        return TutorialStatsSchema(
            upvote_count=obj.upvote_count,
            downvote_count=obj.downvote_count,
            completed_count=obj.completed_count,
            submissions_count=obj.submissions_count,
            is_completed_by_user=obj.is_completed_by_user,
        )


class TutorialSubmissionListFilterSchema(FilterSchema):
    user_id: Optional[UUID] = None
    tutorial_id: Optional[UUID] = None
    provider_user_project_id: Optional[UUID] = None
    provider_id: Annotated[Optional[UUID], FilterLookup(["tutorial__provider_id"])] = None
    status: Annotated[Optional[list[TutorialSubmissionStatus]], FilterLookup(["status__in"])] = None
    created_at: Annotated[Optional[datetime], FilterLookup("created_at__lte")] = None


class CreateTutorialSubmissionSchema(Schema):
    tutorial_id: UUID
    provider_user_project_id: UUID
    code: str


class UpdateTutorialSubmissionSchema(Schema):
    status: TutorialSubmissionStatus
    code: str


class ExecuteTutorialSubmissionSchema(Schema):
    user_id: UUID


class ValidateTutorialSubmissionSchema(Schema):
    user_id: UUID


class TutorialSubmissionListSchema(ModelSchema):
    id: UUID
    status: TutorialSubmissionStatus

    class Meta:
        model = TutorialSubmission
        fields = [
            "created_at",
            "updated_at",
        ]


class TutorialSubmissionDetailSchema(ModelSchema):
    id: UUID
    tutorial_id: UUID
    provider_user_project_id: Optional[UUID]
    status: TutorialSubmissionStatus

    class Meta:
        model = TutorialSubmission
        fields = [
            "code",
            "created_at",
            "updated_at",
        ]


class TutorialSubmissionEventListFilterSchema(FilterSchema):
    user_id: Annotated[Optional[UUID], FilterLookup(["tutorial_submission__user_id"])] = None
    tutorial_submission_id: Optional[UUID] = None
    event_status: Optional[TutorialSubmissionStatus] = None


class CreateTutorialSubmissionEventSchema(Schema):
    event_status: TutorialSubmissionStatus
    exit_code: int
    stdout: str
    error: Optional[str]


class TutorialSubmissionEventSchema(ModelSchema):
    id: UUID
    tutorial_submission_id: UUID
    event_status: TutorialSubmissionStatus
    stdout: str
    error: str

    class Meta:
        model = TutorialSubmissionEvent
        fields = [
            "exit_code",
        ]


class TutorialReviewListFilterSchema(FilterSchema):
    tutorial_id: Optional[UUID] = None
    tutorial_author_id: Annotated[Optional[UUID], FilterLookup(["tutorial__author_id"])] = None


# class TutorialReviewSchema(ModelSchema):
#     id: UUID
