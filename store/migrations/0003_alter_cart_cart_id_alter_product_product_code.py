# Generated by Django 5.1.3 on 2024-12-20 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_cart_cart_id_alter_product_product_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(blank=True, default=167217061173084665553630122573218815369, editable=False, max_length=500, unique=True, verbose_name='Sepet İD'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(default='869443687108', editable=False, max_length=1000, verbose_name='Ürün Kodu'),
        ),
    ]
