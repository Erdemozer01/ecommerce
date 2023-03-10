from django.contrib.auth.models import User
from .models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=Profile)
def update_profile(sender, instance, created, **kwargs):
    if not created:
        User.objects.update(first_name=instance.user.profile.first_name, last_name=instance.user.profile.last_name,
                            email=instance.user.profile.email)
        post_save.connect(update_profile, sender=Profile)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        post_save.connect(create_profile, sender=User)


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()
