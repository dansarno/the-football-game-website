from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Q
from . import models


# @receiver(pre_save, sender=models.GroupMatch)
# def match_result(sender, instance, **kwargs):
#     previous_match_instance = models.GroupMatch.objects.get(pk=instance.pk)
#     new_match_instance = instance
#
#     if previous_match_instance.result == "" and new_match_instance.result != "":
#         correct_outcome = new_match_instance.groupmatchoutcome_set.get(outcome=instance.result)
#         successful_bet_groups = models.GroupMatchBetGroup.objects.filter(Q(match1_bet=correct_outcome) |
#                                                                          Q(match2_bet=correct_outcome) |
#                                                                          Q(match3_bet=correct_outcome) |
#                                                                          Q(match4_bet=correct_outcome) |
#                                                                          Q(match5_bet=correct_outcome) |
#                                                                          Q(match6_bet=correct_outcome) |
#                                                                          Q(match7_bet=correct_outcome) |
#                                                                          Q(match8_bet=correct_outcome) |
#                                                                          Q(match9_bet=correct_outcome) |
#                                                                          Q(match10_bet=correct_outcome) |
#                                                                          Q(match11_bet=correct_outcome) |
#                                                                          Q(match12_bet=correct_outcome) |
#                                                                          Q(match13_bet=correct_outcome) |
#                                                                          Q(match14_bet=correct_outcome) |
#                                                                          Q(match15_bet=correct_outcome) |
#                                                                          Q(match16_bet=correct_outcome) |
#                                                                          Q(match17_bet=correct_outcome) |
#                                                                          Q(match18_bet=correct_outcome) |
#                                                                          Q(match19_bet=correct_outcome) |
#                                                                          Q(match20_bet=correct_outcome) |
#                                                                          Q(match21_bet=correct_outcome) |
#                                                                          Q(match22_bet=correct_outcome)
#                                                                          )
#         for successful_bet_group in successful_bet_groups:
#             successful_bet_group.entry.score += correct_outcome.winning_amount
#             successful_bet_group.entry.save()
#
#     elif previous_match_instance.result != "" and new_match_instance.result == "":
#         correct_outcome = previous_match_instance.groupmatchoutcome_set.get(outcome=previous_match_instance.result)
#         successful_bet_groups = models.GroupMatchBetGroup.objects.filter(Q(match1_bet=correct_outcome) |
#                                                                          Q(match2_bet=correct_outcome) |
#                                                                          Q(match3_bet=correct_outcome) |
#                                                                          Q(match4_bet=correct_outcome) |
#                                                                          Q(match5_bet=correct_outcome) |
#                                                                          Q(match6_bet=correct_outcome) |
#                                                                          Q(match7_bet=correct_outcome) |
#                                                                          Q(match8_bet=correct_outcome) |
#                                                                          Q(match9_bet=correct_outcome) |
#                                                                          Q(match10_bet=correct_outcome) |
#                                                                          Q(match11_bet=correct_outcome) |
#                                                                          Q(match12_bet=correct_outcome) |
#                                                                          Q(match13_bet=correct_outcome) |
#                                                                          Q(match14_bet=correct_outcome) |
#                                                                          Q(match15_bet=correct_outcome) |
#                                                                          Q(match16_bet=correct_outcome) |
#                                                                          Q(match17_bet=correct_outcome) |
#                                                                          Q(match18_bet=correct_outcome) |
#                                                                          Q(match19_bet=correct_outcome) |
#                                                                          Q(match20_bet=correct_outcome) |
#                                                                          Q(match21_bet=correct_outcome) |
#                                                                          Q(match22_bet=correct_outcome)
#                                                                          )
#         for successful_bet_group in successful_bet_groups:
#             successful_bet_group.entry.score -= correct_outcome.winning_amount
#             successful_bet_group.entry.save()
#     elif previous_match_instance.result != "" and new_match_instance.result != "" and \
#             previous_match_instance.result != new_match_instance.result:
#         incorrect_outcome = previous_match_instance.groupmatchoutcome_set.get(outcome=previous_match_instance.result)
#         correct_outcome = new_match_instance.groupmatchoutcome_set.get(outcome=instance.result)
#         previous_successful_bet_groups = models.GroupMatchBetGroup.objects.filter(Q(match1_bet=incorrect_outcome) |
#                                                                                   Q(match2_bet=incorrect_outcome) |
#                                                                                   Q(match3_bet=incorrect_outcome) |
#                                                                                   Q(match4_bet=incorrect_outcome) |
#                                                                                   Q(match5_bet=incorrect_outcome) |
#                                                                                   Q(match6_bet=incorrect_outcome) |
#                                                                                   Q(match7_bet=incorrect_outcome) |
#                                                                                   Q(match8_bet=incorrect_outcome) |
#                                                                                   Q(match9_bet=incorrect_outcome) |
#                                                                                   Q(match10_bet=incorrect_outcome) |
#                                                                                   Q(match11_bet=incorrect_outcome) |
#                                                                                   Q(match12_bet=incorrect_outcome) |
#                                                                                   Q(match13_bet=incorrect_outcome) |
#                                                                                   Q(match14_bet=incorrect_outcome) |
#                                                                                   Q(match15_bet=incorrect_outcome) |
#                                                                                   Q(match16_bet=incorrect_outcome) |
#                                                                                   Q(match17_bet=incorrect_outcome) |
#                                                                                   Q(match18_bet=incorrect_outcome) |
#                                                                                   Q(match19_bet=incorrect_outcome) |
#                                                                                   Q(match20_bet=incorrect_outcome) |
#                                                                                   Q(match21_bet=incorrect_outcome) |
#                                                                                   Q(match22_bet=incorrect_outcome)
#                                                                                   )
#         new_successful_bet_groups = models.GroupMatchBetGroup.objects.filter(Q(match1_bet=correct_outcome) |
#                                                                              Q(match2_bet=correct_outcome) |
#                                                                              Q(match3_bet=correct_outcome) |
#                                                                              Q(match4_bet=correct_outcome) |
#                                                                              Q(match5_bet=correct_outcome) |
#                                                                              Q(match6_bet=correct_outcome) |
#                                                                              Q(match7_bet=correct_outcome) |
#                                                                              Q(match8_bet=correct_outcome) |
#                                                                              Q(match9_bet=correct_outcome) |
#                                                                              Q(match10_bet=correct_outcome) |
#                                                                              Q(match11_bet=correct_outcome) |
#                                                                              Q(match12_bet=correct_outcome) |
#                                                                              Q(match13_bet=correct_outcome) |
#                                                                              Q(match14_bet=correct_outcome) |
#                                                                              Q(match15_bet=correct_outcome) |
#                                                                              Q(match16_bet=correct_outcome) |
#                                                                              Q(match17_bet=correct_outcome) |
#                                                                              Q(match18_bet=correct_outcome) |
#                                                                              Q(match19_bet=correct_outcome) |
#                                                                              Q(match20_bet=correct_outcome) |
#                                                                              Q(match21_bet=correct_outcome) |
#                                                                              Q(match22_bet=correct_outcome)
#                                                                              )
#         for previous_successful_bet_group in previous_successful_bet_groups:
#             previous_successful_bet_group.entry.score -= incorrect_outcome.winning_amount
#             previous_successful_bet_group.entry.save()
#         for new_successful_bet_group in new_successful_bet_groups:
#             new_successful_bet_group.entry.score += correct_outcome.winning_amount
#             new_successful_bet_group.entry.save()


@receiver(post_save, sender=models.GroupMatch)
def match_result(sender, instance, **kwargs):
    correct_outcome = None
    if instance.result:
        correct_outcome = instance.groupmatchoutcome_set.get(choice=instance.result)
    for event in models.History.objects.all():
        if instance == event.outcome.outcome.match:
            if correct_outcome:
                event.outcome.group_match_outcome = correct_outcome
                event.outcome.save()
                event.save()
            else:
                event.outcome.delete()
                event.delete()
            return
    new_outcome = models.Outcome.objects.create(group_match_outcome=correct_outcome)
    models.History.objects.create(outcome=new_outcome)
    return


@receiver(post_save, sender=models.History)
def update_scores(sender, instance, **kwargs):
    for entry in models.Entry.objects.all():
        score_total = 0
        entry_bets = entry.bet_set
        for event in models.History.objects.all():
            if event.outcome in entry_bets:
                score_total += event.outcome.outcome.winning_amount
        entry.score = score_total
        entry.save()


@receiver(post_delete, sender=models.History)
def subtract_scores(sender, instance, **kwargs):
    print("Hello")
