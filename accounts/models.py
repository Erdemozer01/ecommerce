from django.db import models
from django.contrib.auth.models import User


def avatar(instance, filename):
    return 'users/avatar/{0}/{1}'.format(instance.user.profile, filename)


def cover(instance, filename):
    return 'users/cover/{0}/{1}'.format(instance.user.profile, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Kullanıcı Adı', related_name='profile')
    first_name = models.CharField(max_length=150, verbose_name="Ad")
    last_name = models.CharField(max_length=150, verbose_name="Soyad")
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name='Ülke', blank=True)
    city = models.CharField(max_length=100, verbose_name='Şehir', blank=True)
    location = models.CharField(max_length=100, verbose_name='İlçe', blank=True)
    address_type = models.CharField(max_length=100, verbose_name='Adres türü', blank=True, help_text="Ör: Ev")
    address = models.CharField(max_length=250, verbose_name='Adres:', blank=True)
    zip_code = models.CharField(max_length=100, verbose_name='Posta kodu', blank=True)
    phone = models.CharField(max_length=130, verbose_name='Telefon', blank=True, unique=True, null=True)
    birth_day = models.DateField(blank=True, null=True, verbose_name='Doğum Tarihi:')

    created = models.DateTimeField(auto_now=True, verbose_name='Katılma Tarihi', blank=True)



    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = 'profile'
        verbose_name = 'Profil'
        verbose_name_plural = 'Profil'


