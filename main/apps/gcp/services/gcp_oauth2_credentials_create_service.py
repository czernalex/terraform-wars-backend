from typing import Sequence

from google.oauth2.credentials import Credentials


class GCPOAuth2CredentialsCreateService:
    TOKEN_URI = "https://oauth2.googleapis.com/token"

    def create(self, refresh_token: str, client_id: str, client_secret: str, scopes: Sequence[str]) -> Credentials:
        return Credentials(
            # Leaving the token field empty is intentional,
            # as the google library will automatically handle
            # obtaining and refreshing the access token
            token=None,
            refresh_token=refresh_token,
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
            token_uri=self.TOKEN_URI,
        )
