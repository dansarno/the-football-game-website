from django.contrib import admin
from .models import Entry, Team, FinalMatch, Group, GroupMatch, \
    Player, Country, Venue, Tournament, TournamentGoalsOutcome, GroupMatchBet, GroupMatchOutcome, \
    TournamentRedCardsOutcome, TournamentOwnGoalsOutcome, TournamentHattricksOutcome, TournamentBetGroup, \
    FinalBetGroup, FinalFirstGoalOutcome, FinalRefContinentOutcome, FinalGoalsOutcome, FinalYellowCardsOutcome, \
    FinalOwnGoalOutcome, BestTeamsSuccessBetGroup, ToReachSemiFinalOutcome, ToReachFinalOutcome, ToWinOutcome, \
    HighestScoringTeamOutcome, MostYellowCardsOutcome, FastestYellowCardsOutcome, FastestGoalOutcome, \
    GroupWinnerOutcome, GroupWinnerBet, FiftyFiftyOutcome, FiftyFiftyBet, FiftyFiftyQuestion, TopGoalscoringGroupBet, \
    TopGoalScoringGroupOutcome, TopGoalScoringPlayerOutcome, TopGoalscoringPlayerBet
from django.utils.html import format_html


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
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


@admin.register(FinalMatch)
class FinalMatchAdmin(admin.ModelAdmin):
    pass


@admin.register(GroupMatch)
class GroupMatchAdmin(admin.ModelAdmin):
    pass


@admin.register(GroupMatchOutcome)
class GroupMatchOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_code', 'show_flag')

    def show_flag(self, obj):
        return format_html('<img src="{}" width="30"/>'.format(obj.flag.url))

    show_flag.short_description = 'Flag'


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    pass


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    pass


@admin.register(TournamentBetGroup)
class TournamentBetGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(TournamentGoalsOutcome)
class TournamentGoalsOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(TournamentRedCardsOutcome)
class TournamentRedCardsOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(TournamentOwnGoalsOutcome)
class TournamentOwnGoalsOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(TournamentHattricksOutcome)
class TournamentHatricksOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(GroupMatchBet)
class GroupMatchBetAdmin(admin.ModelAdmin):
    pass


@admin.register(FinalBetGroup)
class FinalBetGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(FinalFirstGoalOutcome)
class FinalFirstGoalOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(FinalYellowCardsOutcome)
class FinalYellowCardsOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(FinalOwnGoalOutcome)
class FinalOwnGoalOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(FinalRefContinentOutcome)
class FinalRefContinentOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(FinalGoalsOutcome)
class FinalGoalsOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(BestTeamsSuccessBetGroup)
class BestTeamsSuccessBetGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(ToReachSemiFinalOutcome)
class ToReachSemiFinalOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(ToReachFinalOutcome)
class ToReachFinalOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(ToWinOutcome)
class ToWinOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(HighestScoringTeamOutcome)
class HighestScoringTeamOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(MostYellowCardsOutcome)
class MostYellowCardsOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(FastestYellowCardsOutcome)
class FastestYellowCardsOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(FastestGoalOutcome)
class FastestGoalOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(GroupWinnerOutcome)
class GroupWinnerOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(GroupWinnerBet)
class GroupWinnerBetAdmin(admin.ModelAdmin):
    pass


@admin.register(FiftyFiftyOutcome)
class FiftyFiftyOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(FiftyFiftyBet)
class FiftyFiftyBetAdmin(admin.ModelAdmin):
    pass


@admin.register(FiftyFiftyQuestion)
class FiftyFiftyQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(TopGoalscoringGroupBet)
class TopGoalscoringGroupBetAdmin(admin.ModelAdmin):
    pass


@admin.register(TopGoalScoringGroupOutcome)
class TopGoalScoringGroupOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(TopGoalscoringPlayerBet)
class TopGoalscoringPlayerBetAdmin(admin.ModelAdmin):
    pass


@admin.register(TopGoalScoringPlayerOutcome)
class TopGoalScoringPlayerOutcomeAdmin(admin.ModelAdmin):
    pass
