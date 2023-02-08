import random
import string

from django import forms
from django.contrib import admin

from core import settings


class CustomModelAdmin(admin.ModelAdmin):
    """
    This class inherits admin.ModelAdmin. Purpose of this custom class is to identify the jsonfield which
    needs to add different translated values and add new fields.
    Note: Fields specified as Fieldsets won't support this logic
    """
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.translated_fields = {}

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form = self.modify_initial_data(obj, form)  # for loading data in json to newly created fields
        return form

    def get_fields(self, request, obj=None):
        """
        Helper function to create language wise fields for json field and remove parent field
        """
        gf = list(super().get_fields(request, obj))
        new_dynamic_fields = []
        remove_fields = []
        # one time activity of creating language code wise new fields
        for field_label, field in self.form.base_fields.items():
            if field_label in gf and 'translation_needed' in field.__dict__ and field.translation_needed:
                remove_fields.append(field_label)
                self.translated_fields[field_label] = []
                res = ''.join(random.choices(string.ascii_letters, k=7))  # extra logic to add unique field
                for code, label in settings.LANGUAGES:
                    required = True if code == settings.DEFAULT_LANGUAGE_CODE else False
                    new_dynamic_fields.append((
                        field_label,
                        f'{field_label}_{code}_{res}',
                        forms.CharField(label=f'{field.label} ({code})', required=required)
                    ))
                    self.translated_fields[field_label].append(f'{field_label}_{code}_{res}')
        # Adding newly created fields to field set
        for field in new_dynamic_fields:
            gf.insert(gf.index(field[0]), field[1])
            self.form.declared_fields.update({
                field[1]: field[2]
            })
        # Removing JSON field from base fields and field list
        for field in remove_fields:
            self.form.base_fields.pop(field, None)
            gf.remove(field)
        self.fields = gf
        return gf

    @staticmethod
    def get_language_code(field_name):
        """
        Helper function to get language code from a string
        :param field_name: This value will be in the format field_languageCode_someString
        :return: languageCode
        """
        return field_name.split("_")[1]

    def join_translate_data(self, obj, cleaned_data):
        """
        Helper function to convert field values to json and modify obj
        """
        for field, sub_fields in self.translated_fields.items():
            translated_data = {
                self.get_language_code(item): cleaned_data.pop(item) for item in sub_fields
            }
            cleaned_data[field] = translated_data
            setattr(obj, field, translated_data)
        return obj, cleaned_data

    def save_model(self, request, obj, form, change):
        obj, form.cleaned_data = self.join_translate_data(obj, form.cleaned_data)
        super().save_model(request, obj, form, change)

    def modify_initial_data(self, obj, form):
        """
        Helper function to assign values from json data to respective fields
        """
        if obj:
            for field, sub_fields in self.translated_fields.items():
                obj_data = getattr(obj, field)
                for sub_field in sub_fields:
                    form.declared_fields[sub_field].initial = obj_data.get(self.get_language_code(sub_field))
        else:
            for field_label, field in form.declared_fields.items():
                field.initial = ''
        return form
