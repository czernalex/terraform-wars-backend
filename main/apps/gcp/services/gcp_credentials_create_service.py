from typing import Sequence

from allauth.socialaccount.models import SocialApp, SocialToken
from google.oauth2.credentials import Credentials


class GCPCredentialsCreateService:
    def create(self, social_token: SocialToken, social_app: SocialApp, scopes: Sequence[str]) -> Credentials:
        return Credentials(
            token=None,  # Leaving this field empty is intentional, as the google library will automatically handle obtaining and refreshing the access token
            refresh_token=social_token.token_secret,
            client_id=social_app.client_id,
            client_secret=social_app.secret,
            scopes=scopes,
            token_uri="https://oauth2.googleapis.com/token",
        )
