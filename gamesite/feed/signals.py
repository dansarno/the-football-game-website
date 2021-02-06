from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from enter.models import CalledBet
from . import models


@receiver(post_save, sender=CalledBet)
def create_called_bet_post(sender, instance, created, **kwargs):
    if created:
        models.CalledBetPost.objects.create(bet=instance)


@receiver(post_save, sender=CalledBet)
def save_called_bet_post(sender, instance, **kwargs):
    instance.calledbetpost.save()
