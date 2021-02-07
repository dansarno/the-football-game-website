from django.contrib import admin
from .models import Profile, AccessCode, Team


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'remaining')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass
