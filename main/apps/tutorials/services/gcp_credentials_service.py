from allauth.socialaccount.models import SocialApp, SocialToken
from google.oauth2.credentials import Credentials


class GCPCredentialsService:
    def get_credentials(self, social_token: SocialToken, social_app: SocialApp, scopes: list[str]) -> Credentials:
        return Credentials(
            token=None,
            refresh_token=social_token.token_secret,
            client_id=social_app.client_id,
            client_secret=social_app.secret,
            scopes=scopes,
            token_uri="https://oauth2.googleapis.com/token",
        )
