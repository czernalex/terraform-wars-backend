from django.db import models

from main.apps.tutorials.models import Provider


class ProviderRetrievalService:
    def get_provider_list(self) -> models.QuerySet[Provider]:
        return Provider.objects.all()
