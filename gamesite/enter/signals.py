from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from . import models
from django.core.cache import cache
from users.models import Team
from django.utils import timezone


def recalculate_scores_and_positions_delete(instance):
    called_bets_after_this_one = models.CalledBet.objects.filter(
        date__gt=instance.date).order_by('date')
    previous_called_bet_to_this_one = models.CalledBet.objects.filter(
        date__lt=instance.date).last()
    # only submitted entries can participate in the game
    entries = models.Entry.objects.filter(has_submitted=True)
    if previous_called_bet_to_this_one:
        # Restore scores and positions back to the value before the called bet instance
        for entry in entries:
            entry.current_score = models.ScoreLog.objects. \
                filter(
                    entry=entry, called_bet=previous_called_bet_to_this_one).first().score
            entry.current_position = models.PositionLog.objects. \
                filter(
                    entry=entry, called_bet=previous_called_bet_to_this_one).first().position
            entry.save()
    else:
        # Restore scores back to zero
        entries.update(current_score=0, current_position=None, current_team_position=None, correct_bets=0)
        
        if not called_bets_after_this_one:
            Team.objects.all().update(score=0, position=None)
            return
    
    for called_bet in called_bets_after_this_one:
        
        called_bets_in_same_group = models.CalledBet.objects.filter(outcome__choice_group=called_bet.outcome.choice_group).distinct()

        # 1. Update scores for those that won this called bet
        for entry in entries:
            bet_in_same_group = models.Bet.objects.filter(entry=entry,
                                                          outcome__choice_group=called_bet.outcome.choice_group
                                                          ).first()
            if bet_in_same_group.outcome == called_bet.outcome:
                entry.current_score += called_bet.outcome.winning_amount
                bet_in_same_group.success = True
                bet_in_same_group.called_bet = called_bet
            else:
                if not bet_in_same_group.outcome in [cb.outcome for cb in called_bets_in_same_group]:
                    bet_in_same_group.success = False
                    bet_in_same_group.called_bet = called_bet
            bet_in_same_group.updated_on = timezone.now()
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
        highest_score = ordered_entries[0].current_score
        current_correct_bets = 0
        for i, entry in enumerate(ordered_entries):
            if entry.current_score < highest_score or entry.correct_bets < current_correct_bets:
                position = i + 1
            entry.current_position = position
            entry.save()

            position_log = models.PositionLog.objects.filter(
                entry=entry, called_bet=called_bet).first()
            position_log.position = position
            position_log.save()

            highest_score = entry.current_score
            current_correct_bets = entry.correct_bets

    # 3. Update positions in teams and scores of teams
    teams = Team.objects.all()
    for team in teams:
        position_in_team = 1
        ordered_entries = models.Entry.objects.filter(has_submitted=True, profile__team=team).order_by(
            '-current_score', '-correct_bets', 'profile__user__first_name')
        if not ordered_entries:
            continue
        total_score = 0
        highest_score = ordered_entries[0].current_score
        current_correct_bets = 0
        for i, entry in enumerate(ordered_entries):
            if entry.current_score < highest_score or entry.correct_bets < current_correct_bets:
                position_in_team = i + 1
            entry.current_team_position = position_in_team
            entry.save()
            total_score += entry.current_score
            highest_score = entry.current_score
            current_correct_bets = entry.correct_bets
        team.score = round(total_score / ordered_entries.count())
        team.save()
    
    # 4. Update positions of teams
    position_of_team = 1
    ordered_teams = Team.objects.order_by('-score')
    highest_score = ordered_teams[0].score
    for i, team in enumerate(ordered_teams):
            if team.score < highest_score:
                position_of_team = i + 1
            team.position = position_of_team
            team.save()

            highest_score = team.score


def recalculate_from_instance(instance, created):
    called_bets_including_and_after_this_one = models.CalledBet.objects.filter(
        date__gte=instance.date).order_by('date')
    previous_called_bet_to_this_one = models.CalledBet.objects.filter(
        date__lt=instance.date).order_by('date').last()
    # only submitted entries can participate in the game
    entries = models.Entry.objects.filter(has_submitted=True)
    if previous_called_bet_to_this_one:
        # Restore scores and positions back to the value before the called bet instance
        for entry in entries:
            entry.current_score = models.ScoreLog.objects.\
                filter(
                    entry=entry, called_bet=previous_called_bet_to_this_one).first().score
            entry.current_position = models.PositionLog.objects. \
                filter(
                    entry=entry, called_bet=previous_called_bet_to_this_one).first().position
            entry.save()
    else:
        # Restore scores back to zero
        entries.update(current_score=0, current_position=None, current_team_position=None, correct_bets=0)
    for called_bet in called_bets_including_and_after_this_one:
        called_bets_in_same_group = models.CalledBet.objects.filter(outcome__choice_group=called_bet.outcome.choice_group).distinct()
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
                bet_in_same_group.success = True
                bet_in_same_group.called_bet = called_bet
            else:
                incorrect_count += 1
                # if the bet is not the same as any of the correct answers...
                if not bet_in_same_group.outcome in [cb.outcome for cb in called_bets_in_same_group]:
                    bet_in_same_group.success = False
                    bet_in_same_group.called_bet = called_bet
            bet_in_same_group.updated_on = timezone.now()
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
        highest_score = ordered_entries[0].current_score
        current_correct_bets = 0
        for i, entry in enumerate(ordered_entries):
            if entry.current_score < highest_score or entry.correct_bets < current_correct_bets:
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
            highest_score = entry.current_score
            current_correct_bets = entry.correct_bets

        # 3. Update or create correct and incorrect count stats for the called bet instance
        if created:
            models.CalledBetStats.objects.create(
                called_bet=called_bet, num_correct=correct_count, num_incorrect=incorrect_count)
        else:
            stats = called_bet.calledbetstats
            stats.num_correct = correct_count
            stats.num_incorrect = incorrect_count
            stats.save()
    
    # 4. Update positions in teams and scores of teams
    teams = Team.objects.all()
    for team in teams:
        position_in_team = 1
        ordered_entries = models.Entry.objects.filter(has_submitted=True, profile__team=team).order_by(
            '-current_score', '-correct_bets', 'profile__user__first_name')
        if not ordered_entries:
            continue
        total_score = 0
        highest_score = ordered_entries[0].current_score
        current_correct_bets = 0
        for i, entry in enumerate(ordered_entries):
            if entry.current_score < highest_score or entry.correct_bets < current_correct_bets:
                position_in_team = i + 1
            entry.current_team_position = position_in_team
            entry.save()
            total_score += entry.current_score
            highest_score = entry.current_score
            current_correct_bets = entry.correct_bets
        team.score = round(total_score / ordered_entries.count())
        team.save()

    # 5. Update positions of teams
    position_of_team = 1
    ordered_teams = Team.objects.order_by('-score')
    highest_score = ordered_teams[0].score
    for i, team in enumerate(ordered_teams):
            if team.score < highest_score:
                position_of_team = i + 1
            team.position = position_of_team
            team.save()

            highest_score = team.score


def recalculate_from_beginning(instance):
    called_bets = models.CalledBet.objects.order_by('date')
    entries = models.Entry.objects.filter(has_submitted=True)
    entries.update(current_score=0)
    entries.update(current_position=None)

    models.ScoreLog.objects.all().delete()
    models.PositionLog.objects.all().delete()

    for called_bet in called_bets:
        called_bets_in_same_group = models.CalledBet.objects.filter(outcome__choice_group=called_bet.outcome.choice_group).distinct()
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
                bet_in_same_group.success = True
                bet_in_same_group.called_bet = called_bet
            else:
                incorrect_count += 1
                # if the bet is not the same as any of the correct answers...
                if not bet_in_same_group.outcome in [cb.outcome for cb in called_bets_in_same_group]:
                    bet_in_same_group.success = False
                    bet_in_same_group.called_bet = called_bet
            bet_in_same_group.updated_on = timezone.now()
            bet_in_same_group.save()

            models.ScoreLog.objects.create(
                score=entry.current_score, entry=entry, called_bet=called_bet)

            # Update the number of correct bets each entry has had after this called bet
            num_of_correct_bets = models.Bet.objects.filter(
                entry=entry, success=True).count()
            entry.correct_bets = num_of_correct_bets
            entry.save()

        # 2. Update positions given the new scores
        position = 1
        ordered_entries = models.Entry.objects.filter(has_submitted=True).order_by(
            '-current_score', '-correct_bets', 'profile__user__first_name')
        highest_score = ordered_entries[0].current_score
        current_correct_bets = 0
        for i, entry in enumerate(ordered_entries):
            if entry.current_score < highest_score or entry.correct_bets < current_correct_bets:
                position = i + 1
            entry.current_position = position
            entry.save()

            models.PositionLog.objects.create(
                position=position, entry=entry, called_bet=called_bet)
            
            highest_score = entry.current_score
            current_correct_bets = entry.correct_bets


        # 3. Update correct and incorrect count stats for the called bet
        stats = called_bet.calledbetstats
        stats.num_correct = correct_count
        stats.num_incorrect = incorrect_count
        stats.save()
    
    # 4. Update positions in teams and scores of teams
    teams = Team.objects.all()
    for team in teams:
        total_score = 0
        position_in_team = 1
        ordered_entries = models.Entry.objects.filter(has_submitted=True, profile__team=team).order_by(
            '-current_score', '-correct_bets', 'profile__user__first_name')
        if not ordered_entries:
            continue
        highest_score = ordered_entries[0].current_score
        current_correct_bets = 0
        for i, entry in enumerate(ordered_entries):
            if entry.current_score < highest_score or entry.correct_bets < current_correct_bets:
                position_in_team = i + 1
            entry.current_team_position = position_in_team
            entry.save()
            total_score += entry.current_score
            highest_score = entry.current_score
            current_correct_bets = entry.correct_bets
        team.score = round(total_score / ordered_entries.count())
        team.save()

    # 5. Update positions of teams
    position_of_team = 1
    ordered_teams = Team.objects.order_by('-score')
    highest_score = ordered_teams[0].score
    for i, team in enumerate(ordered_teams):
            if team.score < highest_score:
                position_of_team = i + 1
            team.position = position_of_team
            team.save()

            highest_score = team.score

@receiver(post_save, sender=models.CalledBet)
def updated_called_bets(sender, instance, created, **kwargs):
    recalculate_from_instance(instance, created)
    _invalidate_cached_data("entries_list")
    _invalidate_cached_data("all_history_list")


@receiver(post_delete, sender=models.CalledBet)
def removed_from_called_bets(sender, instance, **kwargs):
    recalculate_scores_and_positions_delete(instance)
    _invalidate_cached_data("entries_list")
    _invalidate_cached_data("all_history_list")

    # Finally update the success statuses of the bets
    other_called_bets_in_same_group = models.CalledBet.objects.filter(outcome__choice_group=instance.outcome.choice_group).distinct()
    if other_called_bets_in_same_group:
        # Update success status of only the bets with this particular outcome
        instance.bet_set.update(success=False)
    else:
        # Clear the success statuses of all bets within the same choice group as the deleted called bet
        models.Bet.objects.filter(
            outcome__choice_group=instance.outcome.choice_group).update(success=None)


@receiver(post_delete, sender=models.Entry)
def recalculate_after_entry_removal(sender, instance, **kwargs):
    if models.CalledBet.objects.all().exists() and instance.has_submitted:
        recalculate_from_beginning(instance)
        _invalidate_cached_data("entries_list")
        _invalidate_cached_data("all_history_list")


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


def _invalidate_cached_data(cache_key):
    cache.delete(cache_key)
