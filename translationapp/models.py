from django.db import models
from django.db.models import JSONField, CharField
from mptt.models import MPTTModel, TreeForeignKey
from core.CustomFields import JsonFieldWithTranslation


# Create your models here.
class SampleModel(models.Model):
    title = JsonFieldWithTranslation()
    article = JsonFieldWithTranslation()
    author = JSONField(default=dict, blank=True, null=True)  # Added just for testing


class MpttSampleModel(MPTTModel):
    name = CharField(max_length=5)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
