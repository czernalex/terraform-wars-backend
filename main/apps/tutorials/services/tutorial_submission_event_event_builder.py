from main.apps.tutorials.schemas import TutorialSubmissionEventEventSchema


class TutorialSubmissionEventEventBuilder:
    def build_event(self, tutorial_submission_event_event: TutorialSubmissionEventEventSchema) -> str:
        return f"event: message\nid: {tutorial_submission_event_event.id}\ndata: {tutorial_submission_event_event.model_dump_json()}\n\n"
