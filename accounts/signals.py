from django.contrib.auth.models import User
from django.conf import settings
from settings.models import SiteSettingModels

from .models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, post_init


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def profile_update(sender, instance, **kwargs):
    Profile.objects.filter(user=instance).update(user=instance, first_name=instance.first_name, last_name=instance.last_name, email=instance.email)


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()



@receiver(post_init, sender=SiteSettingModels)
def update_email_host_user(sender, instance, **kwargs):
    if instance.is_active and instance.theme == 'neumorphism':
        # Aktif bir site ayarı varsa email_host_user güncellemesi yapılır.
        settings.EMAIL_HOST_USER = instance.email
        settings.EMAIL_HOST_PASSWORD = instance.email_password