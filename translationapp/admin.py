from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from core.CustomAdmin import CustomModelAdmin
from .forms import SampleModelForm
from .models import SampleModel, MpttSampleModel


@admin.register(SampleModel)
class SampleModelAdmin(CustomModelAdmin):
    form = SampleModelForm


admin.site.register(MpttSampleModel, MPTTModelAdmin)
