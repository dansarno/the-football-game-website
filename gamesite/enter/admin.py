from django.contrib import admin
from . import models
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from django.utils.html import format_html


@admin.register(models.Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'current_position', 'current_score')
    exclude = ('label',)


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('country', 'show_country_flag', 'show_country_code', 'show_logo', 'group')

    def show_logo(self, obj):
        return format_html('<img src="{}" width="30"/>'.format(obj.logo.url))

    def show_country_flag(self, obj):
        return format_html('<img src="{}" width="30"/>'.format(obj.country.flag.url))

    def show_country_code(self, obj):
        return obj.country.country_code

    show_country_flag.short_description = 'Flag'
    show_logo.short_description = 'Logo'
    show_country_code.short_description = 'Code'


@admin.register(models.FinalMatch)
class FinalMatchAdmin(admin.ModelAdmin):
    pass


class GroupMatchOutcomeInline(admin.TabularInline):
    model = models.GroupMatchOutcome
    max_num = 3
    can_delete = False


@admin.register(models.GroupMatch)
class GroupMatchAdmin(admin.ModelAdmin):
    list_display = ('groupmatch', 'result')
    ordering = ['match_number']

    inlines = [
        GroupMatchOutcomeInline,
    ]


@admin.register(models.GroupMatchOutcome)
class GroupMatchOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_code', 'show_flag')

    def show_flag(self, obj):
        return format_html('<img src="{}" width="30"/>'.format(obj.flag.url))

    show_flag.short_description = 'Flag'


@admin.register(models.Venue)
class VenueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Tournament)
class TournamentAdmin(admin.ModelAdmin):
    pass


# @admin.register(models.TournamentBetGroup)
# class TournamentBetGroupAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(models.TournamentGoalsOutcome)
# class TournamentGoalsOutcomeAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(models.TournamentRedCardsOutcome)
# class TournamentRedCardsOutcomeAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(models.TournamentOwnGoalsOutcome)
# class TournamentOwnGoalsOutcomeAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(models.TournamentHattricksOutcome)
# class TournamentHatricksOutcomeAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(models.GroupMatchBetGroup)
# class GroupMatchBetGroupAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(models.FinalBetGroup)
# class FinalBetGroupAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(models.FinalFirstGoalOutcome)
# class FinalFirstGoalOutcomeAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(models.FinalYellowCardsOutcome)
# class FinalYellowCardsOutcomeAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(models.FinalOwnGoalOutcome)
# class FinalOwnGoalOutcomeAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(models.FinalRefContinentOutcome)
# class FinalRefContinentOutcomeAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(models.FinalGoalsOutcome)
# class FinalGoalsOutcomeAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(models.BestTeamsSuccessBetGroup)
# class BestTeamsSuccessBetGroupAdmin(admin.ModelAdmin):
#     pass


@admin.register(models.ToReachSemiFinalOutcome)
class ToReachSemiFinalOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ToReachFinalOutcome)
class ToReachFinalOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ToWinOutcome)
class ToWinOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.HighestScoringTeamOutcome)
class HighestScoringTeamOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MostYellowCardsOutcome)
class MostYellowCardsOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FastestYellowCardsOutcome)
class FastestYellowCardsOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FastestGoalOutcome)
class FastestGoalOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.GroupWinnerOutcome)
class GroupWinnerOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_success')
    list_filter = ('entry',)

    def get_success(self, obj):
        if obj.success is True:
            return True
        elif obj.success is False:
            return False
        else:
            return None

    get_success.short_description = 'Success'


@admin.register(models.ChoiceGroup)
class ChoiceGroupAdmin(admin.ModelAdmin):
    pass


# @admin.register(models.GroupWinnerBetGroup)
# class GroupWinnerBetGroupAdmin(admin.ModelAdmin):
#     pass

#
# @admin.register(models.GroupWinnerBet)
# class GroupWinnerBetAdmin(admin.ModelAdmin):
#     pass


@admin.register(models.FiftyFiftyOutcome)
class FiftyFiftyOutcomeAdmin(admin.ModelAdmin):
    pass


# @admin.register(models.FiftyFiftyBetGroup)
# class FiftyFiftyBetGroupAdmin(admin.ModelAdmin):
#     pass


@admin.register(models.FiftyFiftyQuestion)
class FiftyFiftyQuestionAdmin(admin.ModelAdmin):
    pass


# @admin.register(models.TopGoalscoringGroupBet)
# class TopGoalscoringGroupBetAdmin(admin.ModelAdmin):
#     pass
#
#
@admin.register(models.TopGoalScoringGroupOutcome)
class TopGoalScoringGroupOutcomeAdmin(admin.ModelAdmin):
    pass
#
#
# @admin.register(models.TopGoalscoringPlayerBet)
# class TopGoalscoringPlayerBetAdmin(admin.ModelAdmin):
#     pass


@admin.register(models.TopGoalScoringPlayerOutcome)
class TopGoalScoringPlayerOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CalledBet)
class CalledBetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'show_winning_amount', 'date')

    def show_winning_amount(self, obj):
        return obj.outcome.winning_amount

    show_winning_amount.short_description = 'Winning Amount'


@admin.register(models.ScoreLog)
class ScoreLogAdmin(admin.ModelAdmin):
    list_filter = ('entry',)
    list_display = ('__str__', 'entry', 'score')


@admin.register(models.PositionLog)
class PositionLogAdmin(admin.ModelAdmin):
    list_filter = ('entry',)
    list_display = ('__str__', 'entry', 'position')


@admin.register(models.Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    pass
