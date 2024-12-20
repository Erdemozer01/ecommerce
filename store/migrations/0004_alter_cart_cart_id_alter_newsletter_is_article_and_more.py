# Generated by Django 5.1.3 on 2024-12-20 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_cart_cart_id_alter_product_product_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(blank=True, default=321334409326049868591793232312736962116, editable=False, max_length=500, unique=True, verbose_name='Sepet İD'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='is_article',
            field=models.BooleanField(default=False, help_text='Son yayınlanan 10 makale gönderiye eklenecektir.', verbose_name='Makale eklensin mi ?'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='is_discount',
            field=models.BooleanField(default=False, help_text='Son güncellenen 10 ürün gönderiye eklenecektir.', verbose_name='Ürün eklensin mi ?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(default='869443624270', editable=False, max_length=1000, verbose_name='Ürün Kodu'),
        ),
    ]
