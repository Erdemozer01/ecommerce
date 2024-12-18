from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from autoslug import AutoSlugField

from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Kategori:')
    slug = AutoSlugField(populate_from='title', unique=True)

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
        return super().get_queryset() \
            .filter(status=Posts.Status.PUBLISHED)


class Posts(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Taslak olarak bırak'
        PUBLISHED = 'PB', 'Yayınla'

    category = models.ForeignKey(Category, verbose_name="Kategori", related_name='post', on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='blog/article/', verbose_name="Gönderi Fotosu:")
    title = models.CharField(max_length=250, verbose_name="Başlık:", blank=False)
    text = CKEditor5Field(verbose_name='İçerik', config_name='extends')
    slug = AutoSlugField(populate_from="title", unique=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Yazar')


    hit_count = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    likes = models.ManyToManyField('auth.User', related_name='post_like', verbose_name="Beğendim", blank=True)
    dislikes = models.ManyToManyField('auth.User', related_name='post_dislike', verbose_name="Beğenmedim", blank=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT,
                              verbose_name='Yayınlanma Durumu')
    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'posts'
        ordering = ['-created']
        verbose_name_plural = 'Gönderi'
        verbose_name = 'Gönderi'


class ArticleImages(models.Model):
    article = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='article_images')
    images = models.ImageField(upload_to="article/images/", verbose_name="Makale resimleri")

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return f"{self.article.title} - Image"

    class Meta:
        db_table = 'article_images'
        verbose_name = 'Makale Resmi'
        verbose_name_plural = 'Makale Resimleri'


class ArticleTags(models.Model):
    article = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='article_tags')
    tags = models.CharField(max_length=255, verbose_name="Etiketler")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')

    def __str__(self):
        return self.tags

    class Meta:
        db_table = 'article_tags'
        verbose_name = 'Makale Etiketleri'
        verbose_name_plural = 'Makale Etiketleri'


