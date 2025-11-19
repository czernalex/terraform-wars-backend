from http import HTTPStatus

from anydi import auto
from ninja import Router

from main.apps.core.types import AuthedHttpRequest
from main.apps.users.models import User
from main.apps.users.schemas import UserDetailSchema, UserUpdateSchema
from main.apps.users.services.user_delete_service import UserDeleteService
from main.apps.users.services.user_update_service import UserUpdateService


users_router = Router()


@users_router.get(
    "/me/",
    url_name="user_detail",
    response={HTTPStatus.OK: UserDetailSchema},
    description="Get the authenticated user",
)
def get_me(request: AuthedHttpRequest) -> User:
    return request.user


@users_router.put(
    "/me/",
    url_name="user_detail",
    response={HTTPStatus.OK: UserDetailSchema},
    description="Update the authenticated user",
)
def update_me(
    request: AuthedHttpRequest, data: UserUpdateSchema, user_update_service: UserUpdateService = auto
) -> User:
    return user_update_service.update_user(request.user.id, data)


@users_router.delete(
    "/me/",
    url_name="user_delete",
    response={HTTPStatus.NO_CONTENT: None},
    description="Delete the authenticated user",
)
def delete_me(request: AuthedHttpRequest, user_delete_service: UserDeleteService = auto) -> None:
    return user_delete_service.delete_user(request.user.id)
