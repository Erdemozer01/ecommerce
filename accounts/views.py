from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import DeleteView
from django.db.models import Sum

from store.models import Product, Cart, CartItems
from .models import Profile
from .forms import UserRegistrationForm, UserEditForm, UserProfileEditForm, UserDeleteForm
from django.contrib.auth.models import User
from django.conf import settings


class UserRegister(generic.CreateView):
    template_name = "registration/sign-up.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("accounts:register")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Başarılı Bir Şekilde Kayıt Oldunuz.')
        return super(UserRegister, self).form_valid(form)


def ProfileUpdateView(request, user):

    if request.user.is_anonymous:
        messages.error(request, "Lütfen giriş yapınız")
        return redirect('login')

    if request.user.username != user:
        messages.error(request, "Yetkisiz işlem")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    profile = get_object_or_404(Profile, user=request.user.id)
    user = get_object_or_404(User, username=request.user.username)
    user_form = UserEditForm(request.POST or None, instance=user)
    profile_form = UserProfileEditForm(request.POST or None, instance=profile)
    product = Product.objects.all()
    cart_total_products = \
        CartItems.objects.filter(cart__cart_id=request.session.session_key).aggregate(Sum('quantity'))[
            'quantity__sum']


    total = 0


    if request.method == "POST":

        if user_form.is_valid():
            user_form.save(commit=False)
            profile, created = Profile.objects.get_or_create(user_id=request.user.id)
            profile.first_name = user_form.cleaned_data['first_name']
            profile.last_name = user_form.cleaned_data['last_name']
            profile.email = user_form.cleaned_data['email']
            profile.save()
            user_form.save()

        elif profile_form.is_valid():
            profile_form.save(commit=False)
            profile, created = Profile.objects.get_or_create(user_id=request.user.id)
            profile.birth_day = profile_form.cleaned_data['birth_day']
            profile.save()
            profile_form.save()

        messages.success(request, "Profil başarıyla güncellendi.")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        user_form = UserEditForm(instance=user)
        profile_form = UserProfileEditForm(instance=profile)


    if request.user.is_authenticated:

        wish_list_products = Product.objects.filter(wish_list__username=request.user)

        price = \
            Product.objects.filter(wish_list__username=request.user, is_discount=False).aggregate(
                Sum('price'))['price__sum']

        discount_price = \
            Product.objects.filter(wish_list__username=request.user, is_discount=True).aggregate(
                Sum('discount_price'))['discount_price__sum']

        if discount_price is not None and price is not None:
            total = discount_price + price
        elif discount_price is not None and price is None:
            total = discount_price
        elif discount_price is None and price is not None:
            total = price

        total = round(total, 3)

        product = Product.objects.all()



    return render(
        request,
        "pages/profil.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "wish_list_products": wish_list_products,
            "total": total,
            "product": product,
            "cart_list": cart_total_products,
        })


class UserDeleteView(DeleteView):
    template_name = "pages/delete.html"
    model = User
    success_url = reverse_lazy("store:store_home")
    form_class = UserDeleteForm


    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            messages.error(request, "Lütfen giriş yapınız")
            return redirect(f'%s?next=/accounts/user-profil/{request.user.pk}/' % settings.LOGIN_URL)

        return super(UserDeleteView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.get_object()
        user.delete()
        return HttpResponseRedirect(self.success_url)



