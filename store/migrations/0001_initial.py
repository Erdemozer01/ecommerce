# Generated by Django 4.1.5 on 2023-02-04 01:57

import autoslug.fields
import ckeditor.fields
import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import store.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='store/products/category/', verbose_name='Kategori Fotosu:')),
                ('title', models.CharField(max_length=100, verbose_name='Kategori:')),
                ('explain', ckeditor.fields.RichTextField(blank=True, verbose_name='Kategori Tanımı:')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Yayınlama Tarihi')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
            ],
            options={
                'verbose_name': 'Kategori',
                'verbose_name_plural': 'Kategori',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='GalleryCategoryChildModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Fotoğraf Kategorisi:')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
            ],
            options={
                'verbose_name': 'Fotoğraf Galerisi',
                'verbose_name_plural': 'Fotoğraf Galerisi',
            },
        ),
        migrations.CreateModel(
            name='HeaderSlideModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='slides/', verbose_name='Foto')),
                ('title', models.CharField(max_length=255, verbose_name='Başlık : ')),
                ('subtitle', models.CharField(max_length=255, verbose_name='Alt Başlık : ')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
            ],
            options={
                'verbose_name': 'Slayt',
                'verbose_name_plural': 'Slayt',
                'db_table': 'slides',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(default=uuid.uuid4, editable=False, max_length=1000, verbose_name='Ürün Kodu')),
                ('title', models.CharField(max_length=250, unique=True, verbose_name='Ürün Adı:')),
                ('brand', models.CharField(max_length=100, verbose_name='Ürün Markası')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Ürün Açıklaması')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True)),
                ('price', models.FloatField(verbose_name='Fiyat')),
                ('new_price', models.FloatField(blank=True, null=True, verbose_name='İndirimli Fiyat')),
                ('stock', models.PositiveIntegerField(verbose_name='stok')),
                ('label', models.CharField(blank=True, max_length=100, verbose_name='Etiket')),
                ('is_available', models.CharField(choices=[('SY', 'Satıştan Kaldırıldı'), ('SV', 'Satışta')], default='SV', max_length=2, verbose_name='Satış Durumu')),
                ('image1', models.ImageField(upload_to=store.models.product_images_upload_to, verbose_name='Foto1')),
                ('image2', models.ImageField(blank=True, help_text='İstege Bağlı', upload_to=store.models.product_images_upload_to, verbose_name='Foto2')),
                ('image3', models.ImageField(blank=True, help_text='İstege Bağlı', upload_to=store.models.product_images_upload_to, verbose_name='Foto3')),
                ('image4', models.ImageField(blank=True, help_text='İstege Bağlı', upload_to=store.models.product_images_upload_to, verbose_name='Foto4')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='store.category', verbose_name='Kategori')),
            ],
            options={
                'verbose_name': 'Ürün',
                'verbose_name_plural': 'Ürünler',
                'db_table': 'product',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='ProductOptionsNameModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Ürün Seçenek Adı')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Ürün')),
            ],
            options={
                'verbose_name': 'Ürün Seçeneği',
                'verbose_name_plural': 'Ürün Seçeneği',
            },
        ),
        migrations.CreateModel(
            name='ProductOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('options', models.CharField(help_text='Ör: Kırmızı Renk', max_length=100, unique=True, verbose_name='Seçenekler')),
                ('option_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productoptionsnamemodel', verbose_name='Seçenek Adı')),
            ],
            options={
                'verbose_name': 'Ürün Seçeneği',
                'verbose_name_plural': 'Ürün Seçenekleri',
            },
        ),
        migrations.CreateModel(
            name='ProductDetailsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('options_name', models.CharField(help_text='Ör: Agırlık', max_length=100, verbose_name='Özellik')),
                ('options', models.CharField(help_text='30kg', max_length=100, verbose_name='Özellik Seçenekleri')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Ürün Başlığı')),
            ],
            options={
                'verbose_name': 'Ürün Ayrıntısı',
                'verbose_name_plural': 'Ürün Ayrıntıları',
            },
        ),
        migrations.CreateModel(
            name='GalleryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Başlık : ')),
                ('image', models.ImageField(upload_to='galeri/', verbose_name='Fotoğraf')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.gallerycategorychildmodel', verbose_name='Kategori')),
            ],
            options={
                'verbose_name': 'Fotoğraf',
                'verbose_name_plural': 'Fotoğraflar',
                'db_table': 'galeri',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(verbose_name='Oy')),
                ('comment', models.TextField(verbose_name='Yorum Yap:')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Yayınlama Tarihi')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('commentator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to=settings.AUTH_USER_MODEL, verbose_name='Yazan:')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='store.product', verbose_name='Ürün:')),
            ],
            options={
                'verbose_name': 'Ürün Yorum',
                'verbose_name_plural': 'Ürün Yorumları',
                'db_table': 'comments',
            },
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['created'], name='product_created_faa237_idx'),
        ),
    ]
