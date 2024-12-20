from django.conf import settings
from settings.models import SiteSettingModels

from django.dispatch import receiver
from django.db.models.signals import post_init



@receiver(post_init, sender=SiteSettingModels)
def update_email_host_user(sender, instance, **kwargs):
    if instance.is_active and instance.theme == 'neumorphism':
        # Aktif bir site ayarı varsa email_host_user güncellemesi yapılır.
        settings.EMAIL_HOST_USER = instance.email
        settings.EMAIL_HOST_PASSWORD = instance.email_password