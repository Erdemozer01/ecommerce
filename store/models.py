from django.db import models
from django.utils import timezone
from autoslug.fields import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


def image_upload_to(instance, filename):
    return 'store/product/image/{file}/{filename}'.format(
        file=instance.slug,
        filename=filename
    )


def extra_image_upload_to(instance, filename):
    return 'store/product/extra_image/{file}/{filename}'.format(
        file=instance.slug,
        filename=filename
    )


class Category(models.Model):
    image = models.ImageField(upload_to=image_upload_to, verbose_name='Kategori Fotosu:', blank=True)
    title = models.CharField(max_length=100, verbose_name='Kategori:', unique=True)
    explain = RichTextField(verbose_name='Kategori Tanımı:', config_name="store", blank=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    publish = models.DateTimeField(default=timezone.now, verbose_name='Yayınlama Tarihi')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'category'
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategori'


class Brand(models.Model):
    image = models.ImageField(upload_to='store/brand/', verbose_name='Marka Fotosu:', blank=True)
    title = models.CharField(max_length=100, verbose_name='Marka:', unique=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    publish = models.DateTimeField(default=timezone.now, verbose_name='Yayınlama Tarihi')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'brand'
        verbose_name = 'Marka'
        verbose_name_plural = 'Marka'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Product.Status.PUBLISHED)


class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'SY', 'Stokta YOK'
        PUBLISHED = 'SV', 'Stokta VAR'

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Yazar')
    category = models.ForeignKey(Category, verbose_name="Kategori", related_name='product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to, verbose_name="Ürün Fotosu:")
    title = models.CharField(max_length=250, verbose_name="Başlık:", blank=False, unique=True)
    text = RichTextUploadingField(verbose_name='Açıklama', blank=False)
    slug = AutoSlugField(populate_from="title", unique=True)

    price = models.FloatField(verbose_name='Fiyat')
    update_price = models.FloatField(verbose_name='Güncel Fiyat', blank=True)
    stock = models.IntegerField(verbose_name='stok')
    is_available = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT,
                                    verbose_name='Stock Durumu')
    likes = models.ManyToManyField('auth.User', related_name='product_like', verbose_name="Beğendim", blank=True)
    whir_list = models.ManyToManyField('auth.User', related_name='ürün_istek', verbose_name="Ürün İstek Listesi",
                                       blank=True)

    extra_image1 = models.ImageField(upload_to=extra_image_upload_to, verbose_name="Slayt1",
                                     blank=True)
    extra_image2 = models.ImageField(upload_to=extra_image_upload_to, verbose_name="Slayt2",
                                     blank=True)
    extra_image3 = models.ImageField(upload_to=extra_image_upload_to, verbose_name="Slayt3",
                                     blank=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'product'
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
        verbose_name = 'Ürün'
        verbose_name_plural = 'Ürünler'
