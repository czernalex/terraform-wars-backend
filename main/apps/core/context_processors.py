from django.http import HttpRequest
from django.utils import timezone


def current_year(request: HttpRequest) -> dict[str, int]:
    return {
        "current_year": timezone.now().year,
    }
