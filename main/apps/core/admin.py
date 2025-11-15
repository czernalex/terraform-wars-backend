from django.db.models import JSONField
from django.contrib.postgres.fields import ArrayField
from django_json_widget.widgets import JSONEditorWidget

from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget


class BaseModelAdmin(ModelAdmin):
    formfield_overrides = {
        ArrayField: {
            "widget": ArrayWidget,
        },
        JSONField: {"widget": JSONEditorWidget},
    }

    compressed_fields = True
    warn_unsaved_form = True
    list_filter_submit = True
    list_filter_sheet = False
    change_form_show_cancel_button = True
