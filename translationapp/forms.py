from django import forms

from .models import SampleModel


class SampleModelForm(forms.ModelForm):
    class Meta:
        model = SampleModel
        fields = '__all__'
