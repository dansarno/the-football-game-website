from django.contrib import admin
from .models import Profile, AccessCode, Team, Prize
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
import csv


def download_csv(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=access_code_export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
download_csv.short_description = "Download selected as csv"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'access_code')


@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'remaining')
    actions = [download_csv]
    list_filter = ('remaining',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'position', 'winning_amount', 'band')
    ordering = ['position']
