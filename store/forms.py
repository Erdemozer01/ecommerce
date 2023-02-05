from django import forms
from .models import Comments, ProductOptionsNameModel, ProductOptions


class ProductOptionsForm(forms.ModelForm):
    class Meta:
        model = ProductOptions
        fields = ['options']


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['rating', 'comment']
