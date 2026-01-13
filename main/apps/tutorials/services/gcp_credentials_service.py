from allauth.socialaccount.models import SocialApp, SocialToken
from google.oauth2.credentials import Credentials


class GCPCredentialsService:
    def get_credentials(self, social_token: SocialToken, social_app: SocialApp, scopes: list[str]) -> Credentials:
        return Credentials(
            token=social_token.token,
            refresh_token=social_token.token_secret,
            client_id=social_app.client_id,
            client_secret=social_app.secret,
            scopes=scopes,
        )
