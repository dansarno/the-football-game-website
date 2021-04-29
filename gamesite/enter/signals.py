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


def recalculate_scores_and_positions_delete(instance):
    called_bets_after_this_one = models.CalledBet.objects.filter(
        date__gt=instance.date).order_by('date')
    previous_called_bet_to_this_one = models.CalledBet.objects.filter(
        date__lt=instance.date).last()
    # only submitted entries can participate in the game
    entries = models.Entry.objects.filter(has_submitted=True)
    if previous_called_bet_to_this_one:
        # Restore scores back to the value before the called bet instance
        for entry in entries:
            entry.current_score = models.ScoreLog.objects. \
                filter(
                    entry=entry, called_bet=previous_called_bet_to_this_one).first().score
            entry.save()
    else:
        # Restore scores back to zero
        entries.update(current_score=0, current_position=None, correct_bets=0)
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
            else:
                bet_in_same_group.success = False
            bet_in_same_group.called_bet = called_bet
            bet_in_same_group.save()

            score_log = models.ScoreLog.objects.filter(
                entry=entry, called_bet=called_bet).first()
            score_log.score = entry.current_score
            score_log.save()

            # Update the number of correct bets each entry has had after this called bet
            num_of_correct_bets = models.Bet.objects.filter(
                entry=entry, success=True).count()
            entry.correct_bets = num_of_correct_bets
            entry.save()

        # 2. Update positions given the new scores
        position = 1
        ordered_entries = models.Entry.objects.filter(has_submitted=True).order_by(
            '-current_score', '-correct_bets', 'profile__user__first_name')
        previous_score = ordered_entries[0].current_score
        for i, entry in enumerate(ordered_entries):
            if entry.current_score < previous_score:
                position = i + 1
            entry.current_position = position
            entry.save()

            position_log = models.PositionLog.objects.filter(
                entry=entry, called_bet=called_bet).first()
            position_log.position = position
            position_log.save()

            previous_score = entry.current_score


def recalculate_from_instance(instance, created):
    called_bets_including_and_after_this_one = models.CalledBet.objects.filter(
        date__gte=instance.date).order_by('date')
    previous_called_bet_to_this_one = models.CalledBet.objects.filter(
        date__lt=instance.date).last()
    # only submitted entries can participate in the game
    entries = models.Entry.objects.filter(has_submitted=True)
    if previous_called_bet_to_this_one:
        # Restore scores back to the value before the called bet instance
        for entry in entries:
            entry.current_score = models.ScoreLog.objects.\
                filter(
                    entry=entry, called_bet=previous_called_bet_to_this_one).first().score
            entry.save()
    else:
        # Restore scores back to zero
        entries.update(current_score=0)
    for called_bet in called_bets_including_and_after_this_one:
        correct_count = 0
        incorrect_count = 0
        # 1. Update scores for those that won this called bet
        for entry in entries:
            bet_in_same_group = models.Bet.objects.filter(entry=entry,
                                                          outcome__choice_group=called_bet.outcome.choice_group
                                                          ).first()
            if bet_in_same_group.outcome == called_bet.outcome:
                correct_count += 1
                entry.current_score += called_bet.outcome.winning_amount
                # entry.save()
                bet_in_same_group.success = True
                bet_in_same_group.called_bet = called_bet
                bet_in_same_group.save()
            elif bet_in_same_group.success:
                incorrect_count += 1
                pass
            else:
                incorrect_count += 1
                bet_in_same_group.success = False
                bet_in_same_group.called_bet = called_bet
                bet_in_same_group.save()

            if created and called_bet == instance:
                models.ScoreLog.objects.create(
                    score=entry.current_score, entry=entry, called_bet=instance)
            else:
                score_log = models.ScoreLog.objects.filter(
                    entry=entry, called_bet=called_bet).first()
                score_log.score = entry.current_score
                score_log.save()

            # Update the number of correct bets each entry has had after this called bet
            num_of_correct_bets = models.Bet.objects.filter(
                entry=entry, success=True).count()
            entry.correct_bets = num_of_correct_bets
            entry.save()

        # 2. Update positions given the new scores
        position = 1
        ordered_entries = models.Entry.objects.filter(has_submitted=True).order_by(
            '-current_score', '-correct_bets', 'profile__user__first_name')
        previous_score = ordered_entries[0].current_score
        for i, entry in enumerate(ordered_entries):
            if entry.current_score < previous_score:
                position = i + 1
            entry.current_position = position
            entry.save()
            if created and called_bet == instance:
                models.PositionLog.objects.create(
                    position=position, entry=entry, called_bet=instance)
            else:
                position_log = models.PositionLog.objects.filter(
                    entry=entry, called_bet=called_bet).first()
                position_log.position = position
                position_log.save()
            previous_score = entry.current_score

        # 3. Update or create correct and incorrect count stats for the called bet instance
        if created:
            models.CalledBetStats.objects.create(
                called_bet=called_bet, num_correct=correct_count, num_incorrect=incorrect_count)
        else:
            stats = called_bet.calledbetstats
            stats.num_correct = correct_count
            stats.num_incorrect = incorrect_count
            stats.save()


@receiver(post_save, sender=models.CalledBet)
def updated_called_bets(sender, instance, created, **kwargs):
    recalculate_from_instance(instance, created)


@receiver(post_delete, sender=models.CalledBet)
def removed_from_called_bets(sender, instance, **kwargs):
    recalculate_scores_and_positions_delete(instance)

    # Finally clear the success statuses
    models.Bet.objects.filter(
        outcome__choice_group=instance.outcome.choice_group).update(success=None)


@receiver(post_save, sender=models.Entry)
def label_entries(sender, instance, created, **kwargs):
    if created:
        all_entries = instance.profile.entries.order_by('id')
        labels = ["A", "B", "C"]
        if len(all_entries) == 1:
            entry = all_entries.first()
            entry.label = None
            entry.save()

        else:
            for entry, label in zip(all_entries, labels):
                entry.label = label
                entry.save()


@receiver(post_delete, sender=models.Entry)
def relabel_entries(sender, instance, **kwargs):
    all_entries = instance.profile.entries.order_by('id')
    labels = ["A", "B", "C"]
    if len(all_entries) == 1:
        entry = all_entries.first()
        entry.label = None
        entry.save()

    else:
        for entry, label in zip(all_entries, labels):
            entry.label = label
            entry.save()
