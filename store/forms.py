from django import forms
from .models import Contact, Subscribe

class PromoCodeForm(forms.Form):
    promo_code = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'İndirim Kodu'}),
                                 label='İndirim Kodu')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['subject', 'name', 'email', 'message']




