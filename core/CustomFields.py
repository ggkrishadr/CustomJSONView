from django.db import models


class JsonFieldWithTranslation(models.JSONField):
    """
    Custom JsonField which inherits JSONField to store text in different languages
    """

    def __init__(self, *args, **kwargs):
        self.translation_needed = True
        super(JsonFieldWithTranslation, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        form_field = super().formfield(**kwargs)
        form_field.__dict__['translation_needed'] = True
        return form_field
