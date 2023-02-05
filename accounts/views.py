from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegistrationForm, UserEditForm, UserCreationForm, ProfileEditForm, UserProfileEditForm


class UserRegister(generic.CreateView):
    template_name = "registration/sign-up.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("accounts:register")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Başarılı Bir Şekilde Kayıt Oldunuz.')
        return super(UserRegister, self).form_valid(form)


