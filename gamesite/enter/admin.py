from django.contrib import admin
from . import models
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from django.utils.html import format_html


@admin.register(models.Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_name', 'has_submitted',
                    'current_position', 'current_score', 'correct_bets')
    exclude = ('label',)
    list_filter = ('has_submitted',)
    search_fields = ('profile__user__first_name', 'profile__user__last_name')

    def get_name(self, obj):
        return f"{obj.profile.user.first_name} {obj.profile.user.last_name}"

    get_name.short_description = 'Name'


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('country', 'show_country_flag',
                    'show_country_code', 'show_logo', 'group', 'is_top_team')
    list_filter = ('group', 'is_top_team')

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
    list_display = ('groupmatch', 'result', 'ko_time')
    ordering = ['ko_time', 'match_number']

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


# @admin.register(models.TournamentBetGroup)
# class TournamentBetGroupAdmin(admin.ModelAdmin):
#     pass
#
#
@admin.register(models.TournamentGoalsOutcome)
class TournamentGoalsOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TournamentPenaltiesOutcome)
class TournamentPenaltiesOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TournamentOwnGoalsOutcome)
class TournamentOwnGoalsOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TournamentGoalsInAGameOutcome)
class TournamentGoalsInAGameOutcomeAdmin(admin.ModelAdmin):
    pass


# @admin.register(models.GroupMatchBetGroup)
# class GroupMatchBetGroupAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.FinalBetGroup)
# class FinalBetGroupAdmin(admin.ModelAdmin):
#     pass
#
#
@admin.register(models.FinalFirstGoalOutcome)
class FinalFirstGoalOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FinalYellowCardsOutcome)
class FinalYellowCardsOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FinalRefCountryOutcome)
class FinalRefContinentOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FinalGoalsOutcome)
class FinalGoalsOutcomeAdmin(admin.ModelAdmin):
    pass



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


@admin.register(models.MostCleanSheetsOutcome)
class MostCleanSheetsOutcomeAdmin(admin.ModelAdmin):
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
    list_display = ('__str__', 'order', 'game_category', 'num_choices', 'choices', 'when_called')
    ordering = ['order']

    def num_choices(self, obj):
        return obj.outcome_set.count()
    
    def choices(self, obj):
        display_str = ""
        for outcome in obj.outcome_set.all():
            display_str += f"{outcome.__str__()};"
        return display_str


@admin.register(models.GameCategory)
class GameCategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order')
    ordering = ['order']


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
    list_display = ('question', 'order')


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
    exclude = ('num_correct', 'num_incorrect')

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
