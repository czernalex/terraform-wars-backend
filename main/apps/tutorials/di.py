from injector import Binder, Module, singleton

from main.apps.tutorials.services import (
    TutorialCreateService,
    TutorialDeleteService,
    TutorialRetrievalService,
    TutorialReviewRetrievalService,
    TutorialSubmissionEventCreateService,
    TutorialSubmissionEventEventBuilder,
    TutorialSubmissionEventHubService,
    TutorialSubmissionEventRetrievalService,
    TutorialSubmissionEventStreamService,
    TutorialSubmissionEventStreamSetupService,
    TutorialSubmissionRetrievalService,
    TutorialSubmissionCreateService,
    TutorialSubmissionUpdateService,
    TutorialSubmissionValidationService,
    TutorialTagRetrievalService,
    TutorialUpdateService,
    TutorialValidationService,
)


class TutorialsModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(TutorialRetrievalService, to=TutorialRetrievalService, scope=singleton)
        binder.bind(TutorialCreateService, to=TutorialCreateService, scope=singleton)
        binder.bind(TutorialUpdateService, to=TutorialUpdateService, scope=singleton)
        binder.bind(TutorialDeleteService, to=TutorialDeleteService, scope=singleton)
        binder.bind(TutorialTagRetrievalService, to=TutorialTagRetrievalService, scope=singleton)
        binder.bind(TutorialSubmissionRetrievalService, to=TutorialSubmissionRetrievalService, scope=singleton)
        binder.bind(TutorialSubmissionCreateService, to=TutorialSubmissionCreateService, scope=singleton)
        binder.bind(TutorialValidationService, to=TutorialValidationService, scope=singleton)
        binder.bind(TutorialSubmissionValidationService, to=TutorialSubmissionValidationService, scope=singleton)
        binder.bind(TutorialReviewRetrievalService, to=TutorialReviewRetrievalService, scope=singleton)
        binder.bind(TutorialSubmissionUpdateService, to=TutorialSubmissionUpdateService, scope=singleton)
        binder.bind(TutorialSubmissionEventStreamService, to=TutorialSubmissionEventStreamService, scope=singleton)
        binder.bind(
            TutorialSubmissionEventRetrievalService, to=TutorialSubmissionEventRetrievalService, scope=singleton
        )
        binder.bind(TutorialSubmissionEventEventBuilder, to=TutorialSubmissionEventEventBuilder, scope=singleton)
        binder.bind(TutorialSubmissionEventHubService, to=TutorialSubmissionEventHubService, scope=singleton)
        binder.bind(
            TutorialSubmissionEventStreamSetupService, to=TutorialSubmissionEventStreamSetupService, scope=singleton
        )
        binder.bind(TutorialSubmissionEventCreateService, to=TutorialSubmissionEventCreateService, scope=singleton)
