from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_json_widget.widgets import JSONEditorWidget

from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget


class BaseModelAdmin(ModelAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    formfield_overrides = {
        ArrayField: {
            "widget": ArrayWidget,
        },
        models.JSONField: {"widget": JSONEditorWidget},
    }

    compressed_fields = True
    warn_unsaved_form = True
    list_filter_submit = True
    list_filter_sheet = False
    change_form_show_cancel_button = True
