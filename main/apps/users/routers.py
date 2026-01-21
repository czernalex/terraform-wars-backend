from http import HTTPStatus

from ninja import Router

from main.di import injector
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
def update_me(request: AuthedHttpRequest, data: UserUpdateSchema) -> User:
    user_update_service = injector.get(UserUpdateService)
    return user_update_service.update(request.user.id, data)


@users_router.delete(
    "/me/",
    url_name="user_delete",
    response={HTTPStatus.NO_CONTENT: None},
    description="Delete the authenticated user",
)
def delete_me(request: AuthedHttpRequest) -> None:
    user_delete_service = injector.get(UserDeleteService)
    return user_delete_service.delete(request.user.id)


# @users_router.get(
#     "/me/notifications/",
#     url_name="user_notification_list",
#     response={HTTPStatus.OK: None},
#     description="Get the authenticated user notifications",
# )
# async def stream_user_notifications(request: AuthedHttpRequest) -> User:
#     response = StreamingHttpResponse(
#         content_type="text/event-stream",
#     )
#     response["Cache-control"] = "no-cache"
#     response["X-Accel-Buffering"] = "no"
#     return response
