from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from store.city import country_list, turkey_cities


class UserRegistrationForm(UserCreationForm):
    terms = forms.BooleanField(required=True, label="Kullanıcı Şartlarını kabul ediyorum.")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'terms']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Bu Email zaten kullanılmakta')
        return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kullanıcı Adı'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adı'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyadı:'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email:'}),
        }


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'created', 'first_name', 'last_name', 'email', ]
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}, choices=country_list),
            'city': forms.Select(attrs={'class': 'form-control'}, choices=turkey_cities),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'address_type': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_day': forms.DateInput(attrs={'type': 'date', 'placeholder': 'gg.aa.yyyy'}, format='%Y-%m-%d'),
        }


class UserDeleteForm(forms.Form):
    is_delete = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', }),
                                   label='Hesabımı silmeyi onaylyorum')


class CheckOutForm(forms.ModelForm):
    country = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ülke'}),
                                choices=country_list, label="Ülke")

    city = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Posta Kodu'}),
                             choices=turkey_cities, label="Şehir")

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'address_type', 'country', 'city', 'location', 'address',
                  'zip_code', 'phone', 'birth_day', ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adı'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyadı:'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email:'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon'}),

            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'address_type': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_day': forms.DateInput(attrs={'type': 'date', }, format='%Y-%m-%d'),
        }
