import logging
from uuid import UUID

from django.utils.translation import gettext as _
from injector import inject
from ninja.errors import ValidationError

from main.apps.core.exceptions import NotFoundError
from main.apps.providers.models import ProviderUserProject
from main.apps.tutorials.enums import TutorialSubmissionStatus
from main.apps.tutorials.models import Tutorial, TutorialSubmission
from main.apps.tutorials.services.tutorial_retrieval_service import TutorialRetrievalService
from main.apps.providers.services import ProviderUserProjectRetrievalService, ProviderUserProjectValidationService
from main.apps.tutorials.schemas import CreateTutorialSubmissionSchema
from main.apps.tutorials.services.tutorial_validation_service import TutorialValidationService
from main.apps.tutorials.types import CreateTutorialSubmissionValidatedData


logger = logging.getLogger(__name__)


class TutorialSubmissionValidationService:
    @inject
    def __init__(
        self,
        tutorial_retrieval_service: TutorialRetrievalService,
        provider_user_project_retrieval_service: ProviderUserProjectRetrievalService,
        provider_user_project_validation_service: ProviderUserProjectValidationService,
        tutorial_validation_service: TutorialValidationService,
    ):
        self._tutorial_retrieval_service = tutorial_retrieval_service
        self._provider_user_project_retrieval_service = provider_user_project_retrieval_service
        self._provider_user_project_validation_service = provider_user_project_validation_service
        self._tutorial_validation_service = tutorial_validation_service

    def _validate_tutorial_exists(self, tutorial_id: UUID) -> Tutorial:
        try:
            return self._tutorial_retrieval_service.get_detail_by_id(tutorial_id)
        except NotFoundError as error:
            logger.warning("Tutorial not found: %(tutorial_id)s", {"tutorial_id": tutorial_id})
            raise ValidationError(
                [
                    {
                        "loc": ["tutorial_id"],
                        "msg": str(error),
                        "type": "value_error",
                    }
                ]
            ) from error

    def _validate_tutorial_accepts_submissions(self, tutorial: Tutorial) -> None:
        return self._tutorial_validation_service.validate_accepts_submissions(tutorial)

    def _validate_provider_user_project_exists(
        self, user_id: UUID, provider_user_project_id: UUID
    ) -> ProviderUserProject:
        try:
            return self._provider_user_project_retrieval_service.get_detail_by_id(user_id, provider_user_project_id)
        except NotFoundError as error:
            logger.warning(
                "Provider user project not found: %(user_id)s and %(provider_user_project_id)s",
                {"user_id": user_id, "provider_user_project_id": provider_user_project_id},
            )
            raise ValidationError(
                [
                    {
                        "loc": ["provider_user_project_id"],
                        "msg": str(error),
                        "type": "value_error",
                    }
                ]
            ) from error

    def _validate_provider_user_project_is_configured(self, provider_user_project: ProviderUserProject) -> None:
        self._provider_user_project_validation_service.validate_is_configured(
            provider_user_project, "provider_user_project_id"
        )

    def _validate_provider_user_project_matches_tutorial_provider(
        self, tutorial: Tutorial, provider_user_project: ProviderUserProject
    ) -> None:
        if tutorial.provider_id != provider_user_project.provider_id:
            raise ValidationError(
                [
                    {
                        "loc": ["provider_user_project_id"],
                        "msg": _("Provider user project does not match tutorial provider"),
                        "type": "value_error",
                    }
                ]
            )

    def validate_create_data(
        self, user_id: UUID, data: CreateTutorialSubmissionSchema
    ) -> CreateTutorialSubmissionValidatedData:
        tutorial = self._validate_tutorial_exists(data.tutorial_id)
        provider_user_project = self._validate_provider_user_project_exists(user_id, data.provider_user_project_id)
        self._validate_provider_user_project_is_configured(provider_user_project)
        self._validate_provider_user_project_matches_tutorial_provider(tutorial, provider_user_project)
        self._validate_tutorial_accepts_submissions(tutorial)
        return CreateTutorialSubmissionValidatedData(
            tutorial=tutorial,
            provider_user_project=provider_user_project,
            code=data.code,
        )

    def validate_can_be_executed(self, tutorial_submission: TutorialSubmission) -> None:
        if tutorial_submission.status != TutorialSubmissionStatus.PENDING:
            raise ValidationError(
                [
                    {
                        "loc": ["status"],
                        "msg": _("Tutorial submission with status %(status)s cannot be executed")
                        % {"status": tutorial_submission.status},
                        "type": "value_error",
                    }
                ]
            )

    def validate_can_be_validated(self, tutorial_submission: TutorialSubmission) -> None:
        if tutorial_submission.status != TutorialSubmissionStatus.EXECUTION_SUCCEEDED:
            raise ValidationError(
                [
                    {
                        "loc": ["status"],
                        "msg": _("Tutorial submission with status %(status)s cannot be validated")
                        % {"status": tutorial_submission.status},
                        "type": "value_error",
                    }
                ]
            )

    def validate_can_be_deleted(self, tutorial_submission: TutorialSubmission) -> None:
        if tutorial_submission.status in [
            TutorialSubmissionStatus.PENDING,
            TutorialSubmissionStatus.EXECUTING,
            TutorialSubmissionStatus.EXECUTION_SUCCEEDED,
            TutorialSubmissionStatus.VALIDATING,
        ]:
            raise ValidationError(
                [
                    {
                        "loc": ["status"],
                        "msg": _(
                            "Tutorial submission with status %(status)s cannot be deleted. It must be in a final state."
                        )
                        % {"status": tutorial_submission.status},
                        "type": "value_error",
                    }
                ]
            )
