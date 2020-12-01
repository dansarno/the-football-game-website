from django.contrib import admin
from .models import Team, FinalMatch, Group, GroupMatch, \
    Player, Country, Venue, Tournament, GroupMatchBet

admin.site.register(Team)
admin.site.register(FinalMatch)
admin.site.register(GroupMatch)
admin.site.register(Group)
admin.site.register(Player)
admin.site.register(Country)
admin.site.register(Venue)
admin.site.register(Tournament)
admin.site.register(GroupMatchBet)
