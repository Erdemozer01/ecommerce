from django.db import models
from django.utils import timezone
from autoslug.fields import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
import uuid
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount


def image_upload_to(instance, filename):
    return 'store/products/cover_image/{file}/{filename}'.format(
        file=instance.slug,
        filename=filename
    )


def product_images_upload_to(instance, filename):
    return 'store/products/product_images/{file}/{filename}'.format(
        file=instance.slug,
        filename=filename
    )


class Category(models.Model):
    image = models.ImageField(upload_to='store/products/category/', verbose_name='Kategori Fotosu:', blank=True)
    title = models.CharField(max_length=100, verbose_name='Kategori:')
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


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Product.Status.IN_STOCK)


class Product(models.Model):
    class Status(models.TextChoices):
        NO_STOCK = 'SY', 'Satıştan Kaldırıldı'
        IN_STOCK = 'SV', 'Satışta'

    category = models.ForeignKey(Category, verbose_name="Kategori", related_name='product_category', on_delete=models.CASCADE)
    product_code = models.CharField(default=uuid.uuid4, editable=False, verbose_name='Ürün Kodu', max_length=1000)
    title = models.CharField(max_length=250, verbose_name="Ürün Adı:", blank=False, unique=True)
    brand = models.CharField(max_length=100, verbose_name='Ürün Markası')
    text = RichTextUploadingField(verbose_name='Ürün Açıklaması', blank=False)
    slug = AutoSlugField(populate_from="title", unique=True)
    hit_count = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    price = models.FloatField(verbose_name='Fiyat')
    new_price = models.FloatField(verbose_name='İndirimli Fiyat', blank=True, null=True)
    stock = models.PositiveIntegerField(verbose_name='stok', editable=True)
    label = models.CharField(max_length=100, verbose_name='Etiket', blank=True)
    is_available = models.CharField(max_length=2, choices=Status.choices, default=Status.IN_STOCK,
                                    verbose_name='Satış Durumu')

    image1 = models.ImageField(upload_to=product_images_upload_to, verbose_name="Foto1")
    image2 = models.ImageField(upload_to=product_images_upload_to, verbose_name="Foto2", blank=True,
                               help_text='İstege Bağlı')
    image3 = models.ImageField(upload_to=product_images_upload_to, verbose_name="Foto3", blank=True,
                               help_text='İstege Bağlı')
    image4 = models.ImageField(upload_to=product_images_upload_to, verbose_name="Foto4", blank=True,
                               help_text='İstege Bağlı')

    likes = models.ManyToManyField('auth.User', verbose_name='Müşteri', related_name='product_liked', blank=True)

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


class ProductOptionsNameModel(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Ürün')
    name = models.CharField(verbose_name='Ürün Seçenek Adı', max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ürün Seçeneği'
        verbose_name_plural = 'Ürün Seçeneği'


class ProductOptions(models.Model):
    option_name = models.ForeignKey(ProductOptionsNameModel, on_delete=models.CASCADE, verbose_name='Seçenek Adı')
    options = models.CharField(max_length=100, verbose_name='Seçenekler', help_text='Ör: Kırmızı Renk', unique=True)

    def __str__(self):
        return str(self.option_name)

    class Meta:
        verbose_name = 'Ürün Seçeneği'
        verbose_name_plural = 'Ürün Seçenekleri'


class ProductDetailsModel(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Ürün Başlığı")
    options_name = models.CharField(max_length=100, verbose_name='Özellik', help_text='Ör: Agırlık')
    options = models.CharField(max_length=100, verbose_name='Özellik Seçenekleri', help_text='30kg')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return self.options_name

    class Meta:
        verbose_name = 'Ürün Ayrıntısı'
        verbose_name_plural = 'Ürün Ayrıntıları'


class HeaderSlideModel(models.Model):
    image = models.ImageField(upload_to='slides/', verbose_name='Foto')
    title = models.CharField(verbose_name='Başlık : ', max_length=255)
    subtitle = models.CharField(verbose_name='Alt Başlık : ', max_length=255)

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'slides'
        verbose_name = 'Slayt'
        verbose_name_plural = 'Slayt'


class GalleryCategoryChildModel(models.Model):
    title = models.CharField(max_length=100, verbose_name='Fotoğraf Kategorisi:', unique=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Fotoğraf Galerisi'
        verbose_name_plural = 'Fotoğraf Galerisi'


class GalleryModel(models.Model):
    category = models.ForeignKey(GalleryCategoryChildModel, on_delete=models.CASCADE, verbose_name='Kategori')
    title = models.CharField(verbose_name='Başlık : ', max_length=255)
    image = models.ImageField(upload_to='galeri/', verbose_name='Fotoğraf')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'galeri'
        verbose_name = 'Fotoğraf'
        verbose_name_plural = 'Fotoğraflar'


class Comments(models.Model):
    commentator = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Yazan:', related_name="post")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Ürün:', related_name="comment")
    rating = models.PositiveIntegerField(verbose_name='Oy')
    comment = models.TextField(verbose_name='Yorum Yap:')

    publish = models.DateTimeField(default=timezone.now, verbose_name='Yayınlama Tarihi')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return str(self.commentator) + ', ' + self.product.title[:40]

    class Meta:
        db_table = 'comments'
        verbose_name = 'Ürün Yorum'
        verbose_name_plural = 'Ürün Yorumları'
