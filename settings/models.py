from django.db import models


class SiteSettings(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=100, verbose_name='Telefon')
    address = models.TextField(verbose_name='Adres:')
    facebook = models.URLField(verbose_name='Facebook')
    instagram = models.URLField(verbose_name='Instagram')
    twitter = models.URLField(verbose_name='Twitter')

    def __str__(self):
        return 'Site Ayarı'

    class Meta:
        db_table = 'ayarlar'
        verbose_name = 'site ayarı'
