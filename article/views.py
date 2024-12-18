from django.shortcuts import redirect, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.contrib import messages
from article.models import Posts, ArticleImages, ArticleTags
from django.db.models import Q
from store.models import Product, CartItems
from django.db.models import Sum
from hitcount.views import HitCountDetailView


class ArticleCategoryView(ListView):
    template_name = "pages/category_list.html"
    model = Posts
    context_object_name = "article_category_list"
    paginate_by = 9

    def get_queryset(self):
        search = self.request.GET.get('search', False)
        if search:
            return Posts.objects.filter(Q(title__icontains=search) | Q(category__title__contains=search))
        else:
            return Posts.objects.filter(category__title__icontains=self.kwargs['category'])

    def get_context_data(self, **kwargs):
        total = 0
        category = self.kwargs['category']
        context = super(ArticleCategoryView, self).get_context_data(**kwargs)
        context['category'] = category
        if self.request.user.is_authenticated:
            context['wish_list_products'] = Product.objects.filter(wish_list__username=self.request.user)

            price = \
                Product.objects.filter(wish_list__username=self.request.user, is_discount=False).aggregate(
                    Sum('price'))[
                    'price__sum']
            discount_price = \
                Product.objects.filter(wish_list__username=self.request.user, is_discount=True).aggregate(
                    Sum('discount_price'))['discount_price__sum']

            if discount_price is not None and price is not None:
                total = discount_price + price
            elif discount_price is not None and price is None:
                total = discount_price
            elif discount_price is None and price is not None:
                total = price
            context['total'] = round(total, 3)

            context['product'] = Product.objects.all()
            cart_total_products = \
                CartItems.objects.filter(cart__cart_id=self.request.session.session_key).aggregate(Sum('quantity'))[
                    'quantity__sum']
            context['cart_total_products'] = cart_total_products
        return context


class ArticleTagsView(ListView):
    template_name = "pages/tags.html"
    model = Posts
    context_object_name = "article_tags_list"
    paginate_by = 9

    def get_queryset(self):
        search = self.request.GET.get('search', False)
        if search:
            return Posts.objects.filter(Q(title__icontains=search) | Q(category__title__contains=search))
        else:
            return Posts.objects.filter(article_tags__tags__icontains=self.kwargs['tags'])

    def get_context_data(self, **kwargs):
        context = super(ArticleTagsView, self).get_context_data(**kwargs)
        total = 0
        if self.request.user.is_authenticated:
            context['wish_list_products'] = Product.objects.filter(wish_list__username=self.request.user)

            price = \
                Product.objects.filter(wish_list__username=self.request.user, is_discount=False).aggregate(
                    Sum('price'))[
                    'price__sum']
            discount_price = \
                Product.objects.filter(wish_list__username=self.request.user, is_discount=True).aggregate(
                    Sum('discount_price'))['discount_price__sum']

            if discount_price is not None and price is not None:
                total = discount_price + price
            elif discount_price is not None and price is None:
                total = discount_price
            elif discount_price is None and price is not None:
                total = price
            context['total'] = round(total, 3)

            context['product'] = Product.objects.all()
            cart_total_products = \
                CartItems.objects.filter(cart__cart_id=self.request.session.session_key).aggregate(Sum('quantity'))[
                    'quantity__sum']
            context['cart_total_products'] = cart_total_products
        context['tags'] = self.kwargs['tags']
        return context


class ArticleListView(ListView):
    template_name = "pages/article_list.html"
    model = Posts
    context_object_name = "post_list"
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get('search', False)
        if search:
            return Posts.objects.filter(Q(title__icontains=search) | Q(category__title__icontains=search))
        else:
            return Posts.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        total = 0
        if self.request.user.is_authenticated:
            context['wish_list_products'] = Product.objects.filter(wish_list__username=self.request.user)

            price = \
                Product.objects.filter(wish_list__username=self.request.user, is_discount=False).aggregate(
                    Sum('price'))[
                    'price__sum']
            discount_price = \
                Product.objects.filter(wish_list__username=self.request.user, is_discount=True).aggregate(
                    Sum('discount_price'))['discount_price__sum']

            if discount_price is not None and price is not None:
                total = discount_price + price
            elif discount_price is not None and price is None:
                total = discount_price
            elif discount_price is None and price is not None:
                total = price
            context['total'] = round(total, 3)

            context['product'] = Product.objects.all()
            cart_total_products = \
                CartItems.objects.filter(cart__cart_id=self.request.session.session_key).aggregate(Sum('quantity'))[
                    'quantity__sum']
            context['cart_total_products'] = cart_total_products
        return context


class ArticleDetailView(HitCountDetailView, DetailView):
    template_name = "pages/article_detail.html"
    model = Posts
    context_object_name = "post"
    count_hit = True

    def get_queryset(self):
        search = self.request.GET.get('search', False)
        if search:
            object_list = Posts.objects.filter(Q(title__icontains=search) | Q(category__title__icontains=search))
            if object_list.exists():
                messages.add_message(self.request, messages.SUCCESS, f'{object_list.count()} Ürün Bulundu.')
                return object_list
            else:
                messages.add_message(self.request, messages.ERROR, 'Aradığınız Ürün Bulunamadı')
                return self.model.objects.all()

        else:
            return Posts.objects.all()



    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        total = 0
        # Navbar_wish_list
        if self.request.user.is_authenticated:
            context['wish_list_products'] = Product.objects.filter(wish_list__username=self.request.user)

            price = \
                Product.objects.filter(wish_list__username=self.request.user, is_discount=False).aggregate(
                    Sum('price'))[
                    'price__sum']
            discount_price = \
                Product.objects.filter(wish_list__username=self.request.user, is_discount=True).aggregate(
                    Sum('discount_price'))['discount_price__sum']

            if discount_price is not None and price is not None:
                total = discount_price + price
            elif discount_price is not None and price is None:
                total = discount_price
            elif discount_price is None and price is not None:
                total = price
            context['total'] = round(total, 3)

            context['product'] = Product.objects.all()
            cart_total_products = \
                CartItems.objects.filter(cart__cart_id=self.request.session.session_key).aggregate(Sum('quantity'))[
                    'quantity__sum']
            context['cart_total_products'] = cart_total_products
        context['article_images'] = ArticleImages.objects.filter(article=self.object.id)
        context['related_posts'] = Posts.objects.filter(category=self.object.category)[:5]
        context['article_tags'] = self.get_object().article_tags.all()
        return context


def post_likes(request, pk):
    post = Posts.objects.get(pk=pk)
    if request.user.is_anonymous:
        messages.error(request, "Lütfen giriş yapınız")
        return redirect(f'{settings.LOGIN_URL}?next=/makale/{pk}/{post.category.title}/{post.slug}/')
    else:

        if post.likes.filter(id=request.user.id).exists():
            messages.add_message(request, messages.WARNING, f"{post.title} zaten beğenmişsiniz")
            if post.dislikes.filter(id=request.user.id).exists():
                post.dislikes.remove(request.user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        elif post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
            post.likes.add(request.user)
            messages.add_message(request, messages.INFO, f"Karar değiştirip {post.title} başlıklı makaleyi beğendiniz")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        post.likes.add(request.user)
        messages.add_message(request, messages.SUCCESS, f"{post.title} beğendiniz")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def post_dislikes(request, pk):
    post = Posts.objects.get(pk=pk)
    if request.user.is_anonymous:
        messages.error(request, "Lütfen giriş yapınız")
        return redirect(f'{settings.LOGIN_URL}?next=/makale/{pk}/{post.category.title}/{post.slug}/')
    else:

        if post.dislikes.filter(id=request.user.id).exists():
            messages.add_message(request, messages.WARNING, f"{post.title} zaten beğenmedinizi biliyoruz :) ")
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        elif post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.dislikes.add(request.user)
            messages.add_message(request, messages.INFO,
                                 f"Karar değiştirip {post.title} başlıklı makaleyi beğenmediniz")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        post.dislikes.add(request.user)
        messages.add_message(request, messages.ERROR, f"{post.title} ürünü beğenmediniz")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


