# Generated by Django 5.1.3 on 2024-12-23 17:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, verbose_name='Ad')),
                ('last_name', models.CharField(max_length=150, verbose_name='Soyad')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('country', models.CharField(blank=True, max_length=100, verbose_name='Ülke')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='Şehir')),
                ('location', models.CharField(blank=True, max_length=100, verbose_name='İlçe')),
                ('address_type', models.CharField(blank=True, help_text='Ör: Ev', max_length=100, verbose_name='Adres türü')),
                ('address', models.CharField(blank=True, max_length=250, verbose_name='Adres:')),
                ('zip_code', models.CharField(blank=True, max_length=100, verbose_name='Posta kodu')),
                ('phone', models.CharField(blank=True, max_length=130, null=True, unique=True, verbose_name='Telefon')),
                ('birth_day', models.DateField(blank=True, null=True, verbose_name='Doğum Tarihi:')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='Katılma Tarihi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı Adı')),
            ],
            options={
                'verbose_name': 'Profil',
                'verbose_name_plural': 'Profil',
                'db_table': 'profile',
            },
        ),
    ]
