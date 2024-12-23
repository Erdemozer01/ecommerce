import os.path
from smtplib import SMTPAuthenticationError

from django.contrib import admin
from django.contrib import messages as messages_info
from django.http import HttpResponseRedirect
from django.utils.timezone import now

from django.conf import settings
from django.contrib import messages
from store.models import Product, ProductImage, ProductCategory, ProductComments, PromoCodeModel, Subscribe, Contact, \
    NewsLetter
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.shortcuts import HttpResponse
from .models import Alert
from django.core import mail
from settings.models import SiteSettingModels


@admin.register(ProductCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    search_fields = ['title']


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 0
    classes = ['collapse']


class ProductCommentAdmin(admin.TabularInline):
    model = ProductComments
    extra = 0
    classes = ['collapse']
    ordering = ['-report_count']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin, ProductCommentAdmin]
    list_display = [
        'category',
        'title',
        'price',
        'money_symbol',
        'discount_price',
        'stock',
        'sale_count',
        'discount',
        'is_discount',
        'updated',
        'created',
    ]
    search_fields = ['category__title', 'title']
    search_help_text = "Kategori ve başlık ile arama"
    list_filter = ['category__title', 'brand', 'is_discount', 'updated', 'created']
    list_editable = ['discount', 'stock']
    ordering = ['-created']
    list_per_page = 25
    actions = ['send_product_email']

    @admin.action(description='Seçtiğiniz ürünleri abonelere gönder')
    def send_product_email(self, request, queryset):
        product_list = queryset.order_by('-updated')

        try:
            neumorphism_site = SiteSettingModels.objects.get(is_active=True, theme__icontains="neumorphism")
            from_email = neumorphism_site.email
        except SiteSettingModels.DoesNotExist:
            neumorphism_site = None

        # E-posta gönderim işlemi
        connection = mail.get_connection()
        connection.open()

        success_count = 0
        failure_count = 0

        if len(Subscribe.objects.all()) == 0:
            messages.error(message="Henüz kimse abone olmadığı için işlem gerçekleştirilemedi", request=request)

        for subscriber in Subscribe.objects.all():
            try:
                subject = "Sizin için seçtiklerimiz"
                template_name = os.path.join(settings.BASE_DIR, "templates", "pages", "product_email.html")
                template = get_template(template_name)
                context = {"product_list": product_list, 'subject': subject, 'neumorphism_site': neumorphism_site,
                           'unsubscribe_email': subscriber.email}
                html_content = template.render(context)
                body = HttpResponse(html_content).content.decode("utf-8")
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=body,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[subscriber.email],
                )
                msg.content_subtype = "html"
                msg.send()
                success_count += 1
            except Exception as e:
                failure_count += 1
                messages.error(request, f"{subscriber.email} adresine e-posta gönderilemedi: {str(e)}")

        if success_count:
            messages.success(request, f"{success_count} aboneye başarıyla e-posta gönderildi.")
        if failure_count:
            messages.warning(request, f"{failure_count} e-posta gönderilemedi.")

        connection.close()


@admin.register(PromoCodeModel)
class PromoCodeModelAdmin(admin.ModelAdmin):
    list_display = ["promo_name", "promo_code", "promo_start_date", "promo_end_date", "created"]
    search_fields = ['promo_code']
    list_editable = ["promo_code", "promo_end_date", ]

    def save_model(self, request, obj, form, change):
        self.object = form.save(commit=False)
        if self.object.promo_end_date is None:
            form.save(commit=False)
            messages_info.error(request, "İndirimin son tarihini belirtmediniz")

        elif now() > self.object.promo_end_date:
            messages_info.error(request, "Kampanya başlangıç ve bitiş tarihini kontrol ediniz !")
            form.save(commit=False)
        else:
            self.object.save()
        return super().save_model(request, obj, form, change)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    model = Subscribe
    list_display = ['email']
    search_fields = ['email']


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    model = NewsLetter
    list_display = ['title', 'created']
    search_fields = ['title']
    search_help_text = "Başlık ile arama"
    list_filter = ['created']
    ordering = ['-created']
    list_per_page = 25
    actions = ['send_email']

    # send_email action
    @admin.action(description='Seçtiğiniz konuyu abonelere e-posta ile gönder')
    def send_email(self, request, queryset):

        try:
            neumorphism_site = SiteSettingModels.objects.get(is_active=True, theme__icontains="neumorphism")
            from_email = neumorphism_site.email
        except SiteSettingModels.DoesNotExist:
            neumorphism_site = None

        # E-posta gönderim işlemi
        try:
            connection = mail.get_connection()
            connection.open()  # Burada bağlantı sorunsuz çalışıp çalışmadığını kontrol ettik
        except Exception as conn_error:
            messages.error(request, f"SMTP bağlantısı başarısız oldu: {conn_error}")
            return HttpResponseRedirect(request.path)

        success_count = 0
        failure_count = 0
        obj = queryset

        if len(queryset) > 1:
            messages.error(message="Sadece bir konu seçebilirsiniz!", request=request)
            return HttpResponseRedirect(request.path)
        elif len(Subscribe.objects.all()) == 0:
            messages.error(message="Henüz kimse abone olmadığı için e-posta gönderilmedi!", request=request)
            return HttpResponseRedirect(request.path)
        else:
            obj = queryset[0]

        for subscriber in Subscribe.objects.all():

            try:

                template_name = os.path.join(settings.BASE_DIR, "templates", "pages", "news.html")
                template = get_template(template_name)
                context = {'obj': obj, 'unsubscribe_email': subscriber.email, 'neumorphism_site': neumorphism_site}
                html_content = template.render(context)
                body = HttpResponse(html_content).content.decode("utf-8")
                msg = EmailMultiAlternatives(
                    subject=obj.title,
                    body=body,
                    from_email=from_email,
                    to=[subscriber.email],
                )
                msg.content_subtype = "html"
                msg.send()
                success_count += 1
            except SMTPAuthenticationError as smtp_error:  # Özel olarak SMTPAuthenticationError için
                messages.error(request, f"Giriş yetkilendirme hatası: {smtp_error}")
                failure_count += 1
                break
            except Exception as e:
                messages.error(request, f"{subscriber.email} adresine e-posta gönderilemedi: {str(e)}")
                failure_count += 1

        if success_count:
            messages.success(request, f"{success_count} aboneye başarıyla e-posta gönderildi.")
        if failure_count:
            messages.warning(request, f"{failure_count} e-posta gönderilemedi.")

        try:
            connection.close()  # Bağlantıyı kapatmak önemli!
        except Exception as e:
            messages.error(request, f"SMTP bağlantısı kapatılamadı: {e}")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ['name', 'subject', 'email', 'created']
    search_fields = ['name', 'subject', 'email']
    search_help_text = "ad, konu veya e-posta ile arama"


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'icon', 'is_publish', 'created']
    list_filter = ['created']
    list_editable = ('is_publish', 'type', 'icon')
