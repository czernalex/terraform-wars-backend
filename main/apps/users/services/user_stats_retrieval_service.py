from uuid import UUID

from main.apps.users.schemas import UserStatsSchema


class UserStatsRetrievalService:
    def get_stats(self, user_id: UUID) -> UserStatsSchema:
        return UserStatsSchema(
            completed_tutorials_count=0,
            configured_provider_user_projects_count=0,
            total_tutorial_submission_count=0,
            successful_tutorial_submission_count=0,
            connected_social_accounts_count=0,
        )
