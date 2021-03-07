from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from enter.models import CalledBet
from . import models


@receiver(post_save, sender=CalledBet)
def create_called_bet_post(sender, instance, created, **kwargs):
    if created:
        title = f"🔔 Result: {instance.outcome}"
        models.Post.objects.create(title=title, content="", author=User.objects.get(username='ros'), post_type='B')


# @receiver(post_save, sender=CalledBet)
# def save_called_bet_post(sender, instance, **kwargs):
#     instance.calledbetpost.save()
