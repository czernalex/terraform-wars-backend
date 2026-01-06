from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDv7(models.Func):
    function = "uuidv7"
    output_field = models.UUIDField()


class UUIDExtractTimestamp(models.Func):
    function = "uuid_extract_timestamp"
    output_field = models.DateTimeField()


class AbstractUUIDModel(models.Model):
    id = models.UUIDField(_("ID"), primary_key=True, default=UUIDv7(), editable=False)

    creation_time = models.GeneratedField(
        expression=UUIDExtractTimestamp("id"),
        output_field=models.DateTimeField(),
        db_persist=True,
    )
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.id)
