from typing import Annotated, Optional
from uuid import UUID

from ninja import Field, FilterLookup, FilterSchema, ModelSchema, Schema

from main.apps.providers.enums import ProviderUserProjectStatus
from main.apps.providers.models import Provider, ProviderUserProject
from main.apps.users.schemas import UserDetailSchema


class ProviderSchema(ModelSchema):
    id: UUID
    short_name: str

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


class ProviderProjectSchema(Schema):
    project_id: str
    project_number: str
    display_name: Optional[str]
    parent_name: Optional[str]
    is_linked_with_provider_user_project: bool


class ProviderDetailSchema(ModelSchema):
    id: UUID
    short_name: str
    setup_instructions: str
    setup_script_instructions: str
    setup_script: str
    setup_checklist: Optional[list[str]]
    validation_script_instructions: str
    validation_script_template: str

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


class ProviderUserProjectListFilterSchema(FilterSchema):
    search: Annotated[
        Optional[str],
        FilterLookup(
            [
                "project_id__icontains",
                "name__icontains",
                "description__icontains",
                "provider__name__icontains",
            ]
        ),
    ] = None
    user_id: Optional[UUID] = None
    provider_id: Optional[UUID] = None
    project_id: Optional[str] = None
    status: Optional[ProviderUserProjectStatus] = None
    configuration_attempts: Annotated[Optional[int], FilterLookup("configuration_attempts__lte")] = Field(
        None, gte=0, lte=ProviderUserProject.MAX_CONFIGURATION_ATTEMPTS
    )


class CreateProviderUserProjectSchema(Schema):
    provider_id: UUID
    project_id: str = Field(..., min_length=1, max_length=255)
    project_number: str = Field(..., min_length=1, max_length=255)
    display_name: Optional[str] = Field(..., min_length=1, max_length=255)


class UpdateProviderUserProjectSchema(Schema):
    name: Optional[str] = Field(..., min_length=1, max_length=255)
    description: Optional[str]
    status: ProviderUserProjectStatus
    configuration_attempts: int = Field(..., gte=0, lte=ProviderUserProject.MAX_CONFIGURATION_ATTEMPTS)
    configuration_error: Optional[str]


class ConfigureProviderUserProjectSchema(Schema):
    user_id: UUID


class ProviderUserProjectListSchema(ModelSchema):
    id: UUID
    provider: ProviderSchema
    user_id: UUID
    status: ProviderUserProjectStatus
    configuration_attempts: int
    project_id: str
    name: str
    description: str
    configuration_error: str

    class Meta:
        model = ProviderUserProject
        fields = ["created_at"]


class ProviderUserProjectDetailSchema(ModelSchema):
    id: UUID
    provider: ProviderSchema
    user: UserDetailSchema
    status: ProviderUserProjectStatus
    configuration_attempts: int
    project_id: str
    name: str
    description: str
    configuration_error: str
    config_data: dict[str, str]

    class Meta:
        model = ProviderUserProject
        fields = [
            "created_at",
        ]
