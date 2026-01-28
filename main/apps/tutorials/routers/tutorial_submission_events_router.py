from ninja import Router

from main.apps.core.types import AuthedHttpRequest


tutorial_submission_events_router = Router()


@tutorial_submission_events_router.get(
    "/{tutorial_submission_id}/events/",
    url_name="tutorial_submission_detail_events_list",
)
async def astream_tutorial_submission_events(request: AuthedHttpRequest) -> None:
    pass
