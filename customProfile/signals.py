from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import CustomUser


def customUser_signal(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='participant')
        instance.groups.add(group)
        CustomUser.objects.create(user=instance)


post_save.connect(customUser_signal, sender=User)

