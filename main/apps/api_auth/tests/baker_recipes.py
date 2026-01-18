from model_bakery.recipe import Recipe, baker

from allauth.socialaccount.models import SocialAccount, SocialApp


social_app_google = Recipe(
    SocialApp,
    provider="google",
    name="Google",
    client_id="test_client_id",
    secret="test_secret",
)

social_account_google = Recipe(
    SocialAccount,
    provider="google",
    uid="test_uid",
    user=baker.make_recipe("main.apps.users.tests.active_user"),
)
