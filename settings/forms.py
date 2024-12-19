from django import forms
from .models import SiteSettingModels


class SiteSettingModelsForm(forms.ModelForm):
    class Meta:
        model = SiteSettingModels
        fields = '__all__'
        widgets = {
            'email_password': forms.PasswordInput(render_value=True),
        }


