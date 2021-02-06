from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from enter.models import CalledBet
from . import models


# @receiver(post_save, sender=CalledBet)
# def post_called_bet(sender, instance, **kwargs):
#     print(instance)
#     models.CalledBetPost.objects.create(bet=instance)
