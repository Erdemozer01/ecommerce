# Generated by Django 5.1.3 on 2024-12-19 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(blank=True, default=21755314598988696187321958357029455497, editable=False, max_length=500, unique=True, verbose_name='Sepet İD'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(default='869443612509', editable=False, max_length=1000, verbose_name='Ürün Kodu'),
        ),
    ]
