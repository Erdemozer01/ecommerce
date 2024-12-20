from django.contrib.auth.models import User
from django.conf import settings
from settings.models import SiteSettingModels

from .models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_init


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

