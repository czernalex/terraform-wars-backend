from model_bakery.recipe import Recipe

from main.apps.users.models import User


active_user = Recipe(
    User,
    is_active=True,
)

inactive_user = Recipe(
    User,
    is_active=False,
)
