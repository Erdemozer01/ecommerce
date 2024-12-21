from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from autoslug import AutoSlugField
from accounts.models import Profile
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation
import uuid
from django.utils.translation import gettext_lazy as _

class ProductCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='Kategori:', unique=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'product_category'
        verbose_name = 'Ürün Kategori'
        verbose_name_plural = 'Ürün Kategorileri'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Product.Status.IN_STOCK)


class Product(models.Model):
    class Status(models.TextChoices):
        NO_STOCK = 'SY', 'Satıştan Kaldırıldı'
        IN_STOCK = 'SV', 'Satışta'

    category = models.ForeignKey(ProductCategory, verbose_name=_("category"), related_name='product_category',
                                 on_delete=models.CASCADE, help_text=_("This is the help text"))
    product_code = models.CharField(default=f"8694436{str(uuid.uuid4().int)[0:5]}", editable=False,
                                    verbose_name=_('product code'),
                                    max_length=1000)
    title = models.CharField(max_length=250, verbose_name=_("Product Title:"), blank=False, unique=True)
    image = models.ImageField(upload_to=f'product/', verbose_name='Ürün Fotosu:')
    brand = models.CharField(max_length=100, verbose_name='Ürün Markası')

    text = CKEditor5Field(verbose_name='Ürün Açıklaması', blank=False, config_name='extends')
    slug = AutoSlugField(populate_from="title", unique=True)
    hit_count = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    price = models.FloatField(verbose_name='Fiyat', help_text="Not: Vergi dahil fiyatı giriniz")
    money_symbol = models.CharField(verbose_name="Para birimi", max_length=100, blank=True, null=True, help_text="TL, $, ")
    discount = models.PositiveSmallIntegerField(default=None, verbose_name="İndirim(%) ",
                                                help_text="Yüzde indirimi girin. 10 girdiğinizde fiyata yüzde 10 indirim uygulanacaktır.",
                                                blank=True, null=True, )
    discount_price = models.FloatField(verbose_name='İndirimli Fiyat', blank=True, null=True, editable=False, )

    is_discount = models.BooleanField(verbose_name="İndirimli ürün ?", default=False, blank=True, editable=False, )

    stock = models.PositiveIntegerField(verbose_name='stok', editable=True)

    sale_count = models.PositiveIntegerField(default=0, verbose_name="Satış adeti",
                                             help_text="Ürünün kaç tane satıldığını gösterir")

    is_available = models.CharField(max_length=2, choices=Status.choices, default=Status.IN_STOCK,
                                    verbose_name='Satış Durumu')

    likes = models.ManyToManyField('auth.User', verbose_name='Ürünü beğenenler', related_name='product_liked',
                                   blank=True)

    dislikes = models.ManyToManyField('auth.User', verbose_name='Ürünü beğenmeyenler', related_name='product_disliked',
                                      blank=True)

    wish_list = models.ManyToManyField('auth.User', verbose_name='İstek listesi', related_name='wish_list', blank=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.label

    class Meta:
        db_table = 'product'
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
        verbose_name = 'Ürün'
        verbose_name_plural = 'Ürünler'

    def save(self, *args, **kwargs):
        if self.discount:
            discount = self.price * (self.discount / 100)
            self.discount_price = round(self.price - discount, 3)
            self.is_discount = True

        else:
            self.discount_price = None
            self.discount = None
            self.is_discount = False

        return super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'product/', verbose_name='Ürün Fotosu:')

    def __str__(self):
        return f"{self.product.title} - Image"

    class Meta:
        db_table = 'product_images'
        get_latest_by = 'image'
        verbose_name = 'Ürün Resmi'
        verbose_name_plural = 'Ürün Resimleri'


class ProductComments(models.Model):
    product = models.ForeignKey(Product, related_name='product_comment', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='comment_username', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Yorum:')

    is_approved = models.BooleanField(default=True, verbose_name="Onaylı yorum")
    report_count = models.PositiveIntegerField(default=0, verbose_name="Kötüye Kullanım bildirim sayısı")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Yorum Tarihi')

    class Meta:
        db_table = 'product_comment'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]
        verbose_name = 'Ürün Yorumu'
        verbose_name_plural = 'Ürün Yorumları'


class Cart(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='carts', verbose_name="Müşteri:",
                                 editable=False, )
    cart_id = models.CharField(
        default=uuid.uuid4().int,
        max_length=500,
        verbose_name='Sepet İD',
        primary_key=False,
        blank=True,
        unique=True,
        editable=False,
    )

    total = models.FloatField(verbose_name='Toplam:', blank=True, null=True, editable=False, )
    app_promo = models.BooleanField(verbose_name="Promosyon uygulandı ? ", default=False, editable=True, )
    promo = models.CharField(max_length=100, blank=True, verbose_name="Kampanya Kodu")

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return str(self.cart_id)

    class Meta:
        verbose_name = 'Sepet'
        verbose_name_plural = "Sepetim"


class CartItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Ürün', related_name='cart_product')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Sepet', )
    quantity = models.PositiveIntegerField(verbose_name='Miktar', default=1, )
    items_total = models.FloatField(verbose_name='Ara Toplam:', blank=True, null=True, editable=False, )

    is_ordered = models.BooleanField(default=False, verbose_name="Satın alındı mı ?")
    is_valid = models.BooleanField(default=False, verbose_name="Sepet Onaylandı mı ?")

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'Ürün'
        verbose_name_plural = "Sepetim"

    def product_code(self):
        return self.product.product_code


class PromoCodeModel(models.Model):
    class PromoType(models.TextChoices):
        PERCENT = 'per', 'Yüzde'
        CASH = 'cash', 'Nakit'

    promo_name = models.CharField(max_length=100, verbose_name='Kampanya Adı')
    promo_desc = models.TextField(verbose_name="Kampanya Açıklaması")
    promo_code = models.CharField(max_length=100, verbose_name="İndirim Kodu", blank=True, null=True)
    promo = models.PositiveIntegerField(verbose_name="İndirim", )
    promo_type = models.CharField(max_length=100, choices=PromoType, default=PromoType.PERCENT,
                                  help_text="İndirimin ugulanma şekli", verbose_name="İndirim Türü")
    promo_start_date = models.DateTimeField(verbose_name="Kampanya Başlangıcı", auto_now_add=True, )
    promo_end_date = models.DateTimeField(blank=True, null=True, verbose_name="İndirimin Son Tarih")
    customer = models.ManyToManyField(Profile, related_name='applied_code',
                                      verbose_name="Kampanyadan Yararlanan Kullanıcılar", blank=True, )

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturuma Tarihi')

    def __str__(self):
        return str(self.promo_code)

    class Meta:
        ordering = ['-created']
        verbose_name = "Promosyon Kodu"
        verbose_name_plural = "Promosyon Kodları"

    def save(self, *args, **kwargs):
        if self.promo_code is None:
            self.promo_code = str(uuid.uuid4())
        super(PromoCodeModel, self).save(*args, **kwargs)


class Contact(models.Model):
    subject = models.CharField(max_length=100, verbose_name="Konu")
    name = models.CharField(max_length=100, verbose_name="Ad Soyad")
    email = models.EmailField(max_length=100, verbose_name="E-posta Adresi")
    message = models.TextField(verbose_name="Mesaj")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "İletişim"
        verbose_name_plural = "İletişim"
        db_table = "contact"
        ordering = ['-created']


class NewsLetter(models.Model):
    title = models.CharField(max_length=100, verbose_name="Konu")
    image = models.ImageField(upload_to="bülten/", verbose_name="Konu Fotosu", null=True, blank=True, )
    context = CKEditor5Field(verbose_name="Mesaj", config_name='extends', null=True, blank=True, )

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "bülten"
        verbose_name_plural = "Bültenler"
        db_table = "news_letter"
        ordering = ['-created']
        get_latest_by = '-created'


class Subscribe(models.Model):
    email = models.EmailField(verbose_name="E-posta Adresi", )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Abonelik"
        verbose_name_plural = "Abonelikler"
        db_table = "subscribe"
