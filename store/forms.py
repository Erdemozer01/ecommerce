from django import forms
from .models import OptionsChildModel


class OptionsModelForm(forms.ModelForm):
    class Meta:
        model = OptionsChildModel
        fields = ['options']
