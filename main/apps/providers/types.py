from dataclasses import dataclass

from main.apps.providers.models import Provider


@dataclass(frozen=True)
class CreateProviderUserProjectValidatedData:
    provider: Provider
