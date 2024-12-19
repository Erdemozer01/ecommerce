# Generated by Django 5.1.3 on 2024-12-18 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_cart_cart_id_alter_product_product_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(blank=True, default=120420765741398055137840374354803404826, editable=False, max_length=500, unique=True, verbose_name='Sepet İD'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(default='869443612408', editable=False, max_length=1000, verbose_name='Ürün Kodu'),
        ),
    ]
