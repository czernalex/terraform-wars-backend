from django.conf import settings
from google.auth import default, impersonated_credentials
from google.auth.credentials import Credentials
from google.oauth2 import service_account


class GCPImpersonatedCredentialsCreateService:
    DEFAULT_LIFETIME_IN_SECONDS = 3600

    def _get_source_credentials(self) -> Credentials:
        if settings.USE_GCP_DEFAULT_CREDENTIALS:
            credentials, _ = default()
            return credentials
        else:
            return service_account.Credentials.from_service_account_file(
                settings.GCP_SERVICE_ACCOUNT_SECRET_KEY, scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )

    def create(self, target_service_account_email: str) -> Credentials:
        source_credentials = self._get_source_credentials()
        return impersonated_credentials.Credentials(
            source_credentials=source_credentials,
            target_principal=target_service_account_email,
            target_scopes=["https://www.googleapis.com/auth/cloud-platform"],
            lifetime=self.DEFAULT_LIFETIME_IN_SECONDS,
        )
