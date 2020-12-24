from django.contrib import admin
from .models import Entry, Team, FinalMatch, Group, GroupMatch, \
    Player, Country, Venue, Tournament, TournamentGoalsOutcome, GroupMatchBet, GroupMatchOutcome, \
    TournamentRedCardsOutcome, TournamentOwnGoalsOutcome, TournamentHattricksOutcome, TournamentBetGroup
from django.utils.html import format_html


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


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
