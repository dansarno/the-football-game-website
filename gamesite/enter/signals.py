from django.db.models.signals import post_save, post_delete, pre_delete
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


def update_all():
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
        entry.current_score = score_total
        entry.save()


def recalculate_scores_and_positions(created, instance):
    called_bets = models.CalledBet.objects.all()
    entries = models.Entry.objects.all()
    entries.update(current_score=0)
    for called_bet in called_bets:
        # 1. Update scores for those that won this called bet
        for entry in entries:
            bet_in_same_group = models.Bet.objects.filter(entry=entry,
                                                          outcome__choice_group=called_bet.outcome.choice_group
                                                          ).first()
            if bet_in_same_group.outcome == called_bet.outcome:
                entry.current_score += called_bet.outcome.winning_amount
                entry.save()
                bet_in_same_group.success = True
                bet_in_same_group.save()
            else:
                bet_in_same_group.success = False
                bet_in_same_group.save()

            if created and called_bet == instance:
                models.ScoreLog.objects.create(score=entry.current_score, entry=entry, called_bet=instance)
            elif called_bet == instance:
                score_log = models.ScoreLog.objects.filter(entry=entry, called_bet=instance).first()
                score_log.score = entry.current_score
                score_log.save()

        # 2. Update positions given the new scores
        position = 1
        ordered_entries = models.Entry.objects.order_by('-current_score', 'profile__user__first_name')
        previous_score = ordered_entries[0].current_score
        for entry in ordered_entries:
            if entry.current_score < previous_score:
                position += 1
            entry.current_position = position
            entry.save()
            if created and called_bet == instance:
                models.PositionLog.objects.create(position=position, entry=entry, called_bet=instance)
            elif called_bet == instance:
                position_log = models.PositionLog.objects.filter(entry=entry, called_bet=instance).first()
                position_log.position = position
                position_log.save()
            previous_score = entry.current_score


def recalculate_scores_and_positions_delete(instance):
    called_bets = models.CalledBet.objects.all()
    entries = models.Entry.objects.all()
    entries.update(current_score=0)
    for called_bet in called_bets:
        # 1. Update scores for those that won this called bet
        for entry in entries:
            bet_in_same_group = models.Bet.objects.filter(entry=entry,
                                                          outcome__choice_group=called_bet.outcome.choice_group
                                                          ).first()
            if bet_in_same_group.outcome == called_bet.outcome:
                entry.current_score += called_bet.outcome.winning_amount
                entry.save()
                bet_in_same_group.success = True
                bet_in_same_group.save()
            else:
                bet_in_same_group.success = False
                bet_in_same_group.save()

            if called_bet == instance:
                score_log = models.ScoreLog.objects.filter(entry=entry, called_bet=instance).first()
                score_log.score = entry.current_score
                score_log.save()

        # 2. Update positions given the new scores
        position = 1
        ordered_entries = models.Entry.objects.order_by('-current_score', 'profile__user__first_name')
        previous_score = ordered_entries[0].current_score
        for entry in ordered_entries:
            if entry.current_score < previous_score:
                position += 1
            entry.current_position = position
            entry.save()
            if called_bet == instance:
                position_log = models.PositionLog.objects.filter(entry=entry, called_bet=instance).first()
                position_log.position = position
                position_log.save()
            previous_score = entry.current_score


def recalculate_from_instance(instance):
    called_bets_after_this_one = models.CalledBet.objects.filter(date__gt=instance.date)
    entries = models.Entry.objects.all()
    for entry in entries:
        entry.current_score = models.ScoreLog.objects.filter(entry=entry, called_bet=instance).first().score \
                              - instance.outcome.winning_amount
        entry.save()
    for called_bet in called_bets_after_this_one:
        # 1. Update scores for those that won this called bet
        for entry in entries:
            bet_in_same_group = models.Bet.objects.filter(entry=entry,
                                                          outcome__choice_group=called_bet.outcome.choice_group
                                                          ).first()
            if bet_in_same_group.outcome == called_bet.outcome:
                entry.current_score += called_bet.outcome.winning_amount
                entry.save()
                bet_in_same_group.success = True
                bet_in_same_group.save()
            else:
                bet_in_same_group.success = False
                bet_in_same_group.save()

            if called_bet == instance:
                score_log = models.ScoreLog.objects.filter(entry=entry, called_bet=instance).first()
                score_log.score = entry.current_score
                score_log.save()

        # 2. Update positions given the new scores
        position = 1
        ordered_entries = models.Entry.objects.order_by('-current_score', 'profile__user__first_name')
        previous_score = ordered_entries[0].current_score
        for entry in ordered_entries:
            if entry.current_score < previous_score:
                position += 1
            entry.current_position = position
            entry.save()
            if called_bet == instance:
                position_log = models.PositionLog.objects.filter(entry=entry, called_bet=instance).first()
                position_log.position = position
                position_log.save()
            previous_score = entry.current_score


@receiver(post_save, sender=models.CalledBet)
def updated_called_bets(sender, instance, created, **kwargs):
    recalculate_scores_and_positions(created, instance)


@receiver(pre_delete, sender=models.CalledBet)
def removed_from_called_bets(sender, instance, **kwargs):
    recalculate_scores_and_positions_delete(instance)

    # update_all()
    #
    # position = 1
    # ordered_entries = models.Entry.objects.order_by('-current_score', 'profile__user__first_name')
    # previous_score = ordered_entries[0].current_score
    # for entry in ordered_entries:
    #     if entry.current_score < previous_score:
    #         position += 1
    #     entry.current_position = position
    #     entry.save()
    #     previous_score = entry.current_score

    # Finally clear the success statuses
    models.Bet.objects.filter(outcome__choice_group=instance.outcome.choice_group).update(success=None)
