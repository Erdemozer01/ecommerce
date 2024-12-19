from django.db import models

class SiteSettingModels(models.Model):
    class Theme(models.TextChoices):
        NEUROMORH = 'neumorphism', 'Neumorphism'

    theme = models.CharField(max_length=100, verbose_name="Site Teması", choices=Theme.choices,)
    name = models.CharField(max_length=100, verbose_name="Site Adı", unique=True, )
    explain = models.TextField(verbose_name="Site Açıklaması", help_text="Kısaca nasıl bir site biraz bahsedin...")
    email = models.EmailField(verbose_name="Email")
    email_password = models.CharField(max_length=128, verbose_name='Email Şifresi',)

    phone = models.CharField(max_length=130, verbose_name="Telefon", blank=True, null=True)
    address = models.CharField(max_length=250, verbose_name="Adres:", blank=True, null=True)

    google_map = models.TextField(verbose_name="Google Haritadaki Konumunuz", help_text="Google Haritadaki iframe bağlantısı", blank=True, null=True)
    url = models.URLField(verbose_name="URL", blank=True, null=True)
    logo = models.ImageField(upload_to="logo/", verbose_name="Logo", blank=True, null=True)
    is_active = models.BooleanField(default=False, verbose_name="Site Aktif mi ?")

    created = models.DateTimeField(auto_now_add=True, verbose_name="oluşturulma tarihi")

    def __str__(self):
        return self.theme or self.name or "Site Ayarı"

    class Meta:
        verbose_name = "Site Ayarı"
        verbose_name_plural = "Site Ayarları"


class SiteSettingMeta(models.Model):
    meta = models.ForeignKey(SiteSettingModels, on_delete=models.CASCADE, verbose_name="Ayarlar",
                             related_name='meta_tags')
    description = models.CharField(max_length=100, verbose_name="Özellik adı", blank=True, null=True,
                                   help_text="Social tags")
    name = models.CharField(max_length=100, verbose_name="Meta Adı:")
    content = models.TextField(verbose_name="İçerik")

    def __str__(self):
        return str(self.meta.name)

    class Meta:
        verbose_name = "Meta Tags Ayarı"
        verbose_name_plural = "Meta Tags Ayarları"


class SiteSettingsAboutModels(models.Model):
    about = models.ForeignKey(SiteSettingModels, on_delete=models.CASCADE, verbose_name="Hakkımızda",
                              related_name='about', blank=True, null=True)
    title = models.CharField(max_length=100, verbose_name="Başlık")
    content = models.TextField(verbose_name="Açıklama")
    created = models.DateTimeField(auto_now_add=True, verbose_name="oluşturulma tarihi")

    def __str__(self):
        return self.about.name

    class Meta:
        verbose_name = "Hakkımızda"
        verbose_name_plural = "Hakkımızda"


class SiteSettingsTeamsModels(models.Model):
    teams = models.ForeignKey(SiteSettingModels, on_delete=models.CASCADE, verbose_name="Takım Arkadaşlarımız",
                              related_name='teams', blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Ad Soyad", blank=True, null=True)
    job = models.CharField(max_length=100, verbose_name="Görevi", blank=True, null=True)

    class Meta:
        verbose_name = "Takım Arkadaşı"
        verbose_name_plural = "Takım Arkadaşları"


class SiteSettingsFqModels(models.Model):
    fq = models.ForeignKey(SiteSettingModels, on_delete=models.CASCADE, verbose_name="Sıkça sorulan sorular",
                           related_name='fq', blank=True, null=True)
    question = models.CharField(max_length=100, verbose_name="Soru", blank=True, null=True, help_text="Soru")
    answer = models.TextField(verbose_name="Cevap", blank=True, null=True, help_text="Cevap")

    class Meta:
        verbose_name = "Sıkça sorulan soru"
        verbose_name_plural = "Sıkça sorulan sorular"


class SiteSettingsSocialMedialModels(models.Model):
    social_media = models.ForeignKey(SiteSettingModels, on_delete=models.CASCADE, verbose_name="Sosyal Medya",
                                     related_name='social_media', blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Sosyal medya adı",
                            help_text="Facebook, Twitter, Instagram, Youtube, Linkedin, Pinterest, Github, Google+...")
    link = models.URLField(verbose_name="Link", help_text="Sosyal medya linki", blank=True, null=True)

    class Meta:
        verbose_name = "Sosyal Medya"
        verbose_name_plural = "Sosyal Medya"


class SiteSettingsLicenseModels(models.Model):
    license = models.ForeignKey(SiteSettingModels, on_delete=models.CASCADE, verbose_name="Gizlilik",
                                related_name='prensible', blank=True, null=True)
    text = models.TextField(verbose_name="Gizlilik ilkesi", blank=True, null=True)

    class Meta:
        verbose_name = "Gizlilik ilkesi"
        verbose_name_plural = "Gizlilik ilkesi"
