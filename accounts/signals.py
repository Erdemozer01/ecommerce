from django.contrib.auth.models import User
from django.db import IntegrityError, transaction

from .models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if not created:
        try:
            with transaction.atomic():
                Profile.objects.create(user=instance)
        except:

            Profile.objects.update(user=instance, first_name=instance.first_name, last_name=instance.last_name,
                                   email=instance.email)


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()
