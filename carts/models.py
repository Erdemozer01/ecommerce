import uuid

from store.models import Product
from accounts.models import Profile

from django.db import models


class Cart(models.Model):
    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Müşteri:')
    cart_id = models.CharField(
        default=uuid.uuid4().int,
        max_length=500,
        verbose_name='Sepet İD',
        primary_key=False,
        blank=True
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return str(self.customer.username)

    class Meta:
        verbose_name = 'Sepet'
        verbose_name_plural = 'Sepet'


class CartItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Ürün')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Sepet')
    quantity = models.IntegerField(verbose_name='Miktar')
    total = models.FloatField(verbose_name='Toplam:', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'Ürün'
        verbose_name_plural = 'Sepetim'
