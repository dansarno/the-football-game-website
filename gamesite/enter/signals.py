from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from . import models


@receiver(post_save, sender=models.GroupMatch)
def match_result(sender, instance, **kwargs):
    pass
    # correct_outcome = None
    # if instance.result:
    #     correct_outcome = instance.groupmatchoutcome_set.get(choice=instance.result)
    # for event in models.CalledBet.objects.all():
    #     if instance == event.get_outcome().match:
    #         if correct_outcome:
    #             event.outcome.group_match_outcome = correct_outcome
    #             event.outcome.save()
    #             event.save()
    #         else:
    #             event.outcome.delete()
    #             event.delete()
    #         return
    # new_outcome = models.Outcome.objects.create(group_match_outcome=correct_outcome)
    # models.CalledBet.objects.create(outcome=new_outcome)
    # return


@receiver(post_save, sender=models.CalledBet)
def update_scores(sender, instance, **kwargs):
    events = models.CalledBet.objects.all()
    for entry in models.Entry.objects.all():
        score_total = 0
        for bet in models.Bet.objects.filter(entry=entry):
            if bet.outcome in [event.outcome for event in events]:
                score_total += bet.outcome.winning_amount
                bet.success = True
                bet.save()
        entry.score = score_total
        entry.save()


@receiver(post_delete, sender=models.CalledBet)
def reduce_scores(sender, instance, **kwargs):
    events = models.CalledBet.objects.all()
    for entry in models.Entry.objects.all():
        score_total = 0
        for bet in models.Bet.objects.filter(entry=entry):
            if bet.outcome in [event.outcome for event in events]:
                score_total += bet.outcome.winning_amount
                bet.success = True
                bet.save()
        entry.score = score_total
        entry.save()
    # Finally clear the success statuses
    for bets_of_deleted_outcome in models.Bet.objects.filter(outcome=instance.outcome):
        bets_of_deleted_outcome.success = None
        bets_of_deleted_outcome.save()
