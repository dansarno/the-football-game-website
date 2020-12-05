from django.contrib import admin
from .models import Team, FinalMatch, Group, GroupMatch, \
    Player, Country, Venue, Tournament, GroupMatchBet


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(FinalMatch)
class FinalMatchAdmin(admin.ModelAdmin):
    pass


@admin.register(GroupMatch)
class GroupMatchAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_code', 'flag')


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    pass


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    pass


@admin.register(GroupMatchBet)
class GroupMatchBetAdmin(admin.ModelAdmin):
    pass
