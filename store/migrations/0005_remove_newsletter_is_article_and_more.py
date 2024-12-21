# Generated by Django 5.1.3 on 2024-12-21 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_cart_cart_id_alter_newsletter_is_article_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsletter',
            name='is_article',
        ),
        migrations.RemoveField(
            model_name='newsletter',
            name='is_discount',
        ),
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(blank=True, default=115772187944290274886352254908541153846, editable=False, max_length=500, unique=True, verbose_name='Sepet İD'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(default='869443629525', editable=False, max_length=1000, verbose_name='Ürün Kodu'),
        ),
    ]