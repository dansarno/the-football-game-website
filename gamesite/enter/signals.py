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
    called_bets = models.CalledBet.objects.all()
    entries = models.Entry.objects.all()
    for entry in entries:
        score_total = 0
        for called_bet in called_bets:
            bet_in_same_group = models.Bet.objects.filter(entry=entry,
                                                          outcome__choice_group=called_bet.outcome.choice_group
                                                          ).first()
            if bet_in_same_group.outcome == called_bet.outcome:
                score_total += called_bet.outcome.winning_amount
                bet_in_same_group.success = True
                bet_in_same_group.save()
            else:
                bet_in_same_group.success = False
                bet_in_same_group.save()
        entry.score = score_total
        entry.save()

    position = 1
    ordered_entries = models.Entry.objects.order_by('-score', 'profile__user__first_name')
    previous_score = ordered_entries[0].score
    for entry in ordered_entries:
        if entry.score < previous_score:
            position += 1
        entry.position = position
        entry.save()
        previous_score = entry.score


@receiver(post_delete, sender=models.CalledBet)
def reduce_scores(sender, instance, **kwargs):
    called_bets = models.CalledBet.objects.all()
    entries = models.Entry.objects.all()
    for entry in entries:
        score_total = 0
        for called_bet in called_bets:
            bet_in_same_group = models.Bet.objects.filter(entry=entry,
                                                          outcome__choice_group=called_bet.outcome.choice_group
                                                          ).first()
            if bet_in_same_group.outcome == called_bet.outcome:
                score_total += called_bet.outcome.winning_amount
                bet_in_same_group.success = True
                bet_in_same_group.save()
            else:
                bet_in_same_group.success = False
                bet_in_same_group.save()
        entry.score = score_total
        entry.save()

    position = 1
    ordered_entries = models.Entry.objects.order_by('-score', 'profile__user__first_name')
    previous_score = ordered_entries[0].score
    for entry in ordered_entries:
        if entry.score < previous_score:
            position += 1
        entry.position = position
        entry.save()
        previous_score = entry.score

    # Finally clear the success statuses
    for bet_in_same_group in models.Bet.objects.filter(outcome__choice_group=instance.outcome.choice_group):
        bet_in_same_group.success = None
        bet_in_same_group.save()
