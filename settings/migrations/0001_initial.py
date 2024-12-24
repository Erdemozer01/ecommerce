# Generated by Django 5.1.3 on 2024-12-23 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettingModels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(choices=[('neumorphism', 'Neumorphism')], max_length=100, verbose_name='Site Teması')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Site Adı')),
                ('explain', models.TextField(help_text='Kısaca nasıl bir site biraz bahsedin...', verbose_name='Site Açıklaması')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('email_password', models.CharField(max_length=128, verbose_name='Email Şifresi')),
                ('phone', models.CharField(blank=True, max_length=130, null=True, verbose_name='Telefon')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='Adres:')),
                ('google_map', models.TextField(blank=True, help_text='Google Haritadaki iframe bağlantısı', null=True, verbose_name='Google Haritadaki Konumunuz')),
                ('url', models.URLField(blank=True, null=True, verbose_name='URL')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo/', verbose_name='Logo')),
                ('is_active', models.BooleanField(default=False, verbose_name='Site Aktif mi ?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='oluşturulma tarihi')),
            ],
            options={
                'verbose_name': 'Site Ayarı',
                'verbose_name_plural': 'Site Ayarları',
            },
        ),
        migrations.CreateModel(
            name='SiteSettingMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, help_text='Social tags', max_length=100, null=True, verbose_name='Özellik adı')),
                ('name', models.CharField(max_length=100, verbose_name='Meta Adı:')),
                ('content', models.TextField(verbose_name='İçerik')),
                ('meta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meta_tags', to='settings.sitesettingmodels', verbose_name='Ayarlar')),
            ],
            options={
                'verbose_name': 'Meta Tags Ayarı',
                'verbose_name_plural': 'Meta Tags Ayarları',
            },
        ),
        migrations.CreateModel(
            name='SiteSettingsAboutModels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Başlık')),
                ('content', models.TextField(verbose_name='Açıklama')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='oluşturulma tarihi')),
                ('about', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='about', to='settings.sitesettingmodels', verbose_name='Hakkımızda')),
            ],
            options={
                'verbose_name': 'Hakkımızda',
                'verbose_name_plural': 'Hakkımızda',
            },
        ),
        migrations.CreateModel(
            name='SiteSettingsFqModels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, help_text='Soru', max_length=100, null=True, verbose_name='Soru')),
                ('answer', models.TextField(blank=True, help_text='Cevap', null=True, verbose_name='Cevap')),
                ('fq', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fq', to='settings.sitesettingmodels', verbose_name='Sıkça sorulan sorular')),
            ],
            options={
                'verbose_name': 'Sıkça sorulan soru',
                'verbose_name_plural': 'Sıkça sorulan sorular',
            },
        ),
        migrations.CreateModel(
            name='SiteSettingsLicenseModels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Gizlilik ilkesi')),
                ('license', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prensible', to='settings.sitesettingmodels', verbose_name='Gizlilik')),
            ],
            options={
                'verbose_name': 'Gizlilik ilkesi',
                'verbose_name_plural': 'Gizlilik ilkesi',
            },
        ),
        migrations.CreateModel(
            name='SiteSettingsSocialMedialModels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Facebook, Twitter, Instagram, Youtube, Linkedin, Pinterest, Github, Google+...', max_length=100, verbose_name='Sosyal medya adı')),
                ('link', models.URLField(blank=True, help_text='Sosyal medya linki', null=True, verbose_name='Link')),
                ('social_media', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='social_media', to='settings.sitesettingmodels', verbose_name='Sosyal Medya')),
            ],
            options={
                'verbose_name': 'Sosyal Medya',
                'verbose_name_plural': 'Sosyal Medya',
            },
        ),
        migrations.CreateModel(
            name='SiteSettingsTeamsModels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ad Soyad')),
                ('job', models.CharField(blank=True, max_length=100, null=True, verbose_name='Görevi')),
                ('teams', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='settings.sitesettingmodels', verbose_name='Takım Arkadaşlarımız')),
            ],
            options={
                'verbose_name': 'Takım Arkadaşı',
                'verbose_name_plural': 'Takım Arkadaşları',
            },
        ),
    ]
