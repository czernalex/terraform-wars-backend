from typing import Annotated, Optional
from uuid import UUID

from ninja import Field, FilterLookup, FilterSchema, ModelSchema, Schema

from main.apps.providers.enums import ProviderUserProjectStatus
from main.apps.providers.models import Provider, ProviderUserProject
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


class ProviderProjectSchema(Schema):
    project_id: Optional[str]
    project_name: Optional[str]
    display_name: Optional[str]
    parent_name: Optional[str]


class ProviderDetailSchema(ModelSchema):
    id: UUID
    projects: list[ProviderProjectSchema]

    class Meta:
        model = Provider
        fields = [
            "name",
            "slug",
            "description",
            "website_url",
            "setup_instructions",
            "setup_script",
            "created_at",
            "updated_at",
        ]

    @staticmethod
    def resolve_projects(provider: Provider, context: dict) -> list[ProviderProjectSchema]:
        from main.di import injector
        from main.apps.providers.services import ProviderProjectListServiceFactory

        user_id = context["request"].user.id
        factory = injector.get(ProviderProjectListServiceFactory)
        provider_project_list_service = factory.get_service(provider)
        return provider_project_list_service.get_list(user_id)


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
    status: Optional[ProviderUserProjectStatus] = None
    configuration_attempts: Annotated[Optional[int], FilterLookup("configuration_attempts__lte")] = Field(
        None, gte=0, lte=ProviderUserProject.MAX_CONFIGURATION_ATTEMPTS
    )


class GCPProviderUserProjectConfigDataSchema(Schema):
    gcp_project_id: str
    gcp_project_name: str
    gcp_service_account_email: str


class CreateProviderUserProjectSchema(Schema):
    provider_id: UUID
    project_id: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str]
    config_data: (
        GCPProviderUserProjectConfigDataSchema  # When other providers are supported, they will be added as union type
    )


class UpdateProviderUserProjectSchema(Schema):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str]
    status: ProviderUserProjectStatus
    configuration_attempts: int = Field(..., gte=0, lte=ProviderUserProject.MAX_CONFIGURATION_ATTEMPTS)


class ConfigureProviderUserProjectSchema(Schema):
    user_id: UUID


class ProviderUserProjectListSchema(ModelSchema):
    id: UUID
    provider: ProviderSchema
    user_id: UUID

    class Meta:
        model = ProviderUserProject
        fields = [
            "project_id",
            "name",
            "description",
        ]


class ProviderUserProjectDetailSchema(ModelSchema):
    id: UUID
    provider: ProviderSchema
    user: UserDetailSchema

    class Meta:
        model = ProviderUserProject
        fields = [
            "config_data",
        ]
