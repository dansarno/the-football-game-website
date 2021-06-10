from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
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


class MyUserAdmin(UserAdmin):
    # override the default sort column
    ordering = ['-date_joined']
    # if you want the date they joined or other columns displayed in the list,
    # override list_display too
    list_display = ('username', 'email', 'date_joined', 'first_name', 'last_name')
    list_filter = []

# finally replace the default UserAdmin with yours
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_name', 'access_code')
    search_fields = ('user__first_name', 'user__last_name')

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_name.short_description = 'Name'


@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'remaining')
    actions = [download_csv]
    list_filter = ('remaining',)
    search_fields = ('code',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'score')


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'position', 'winning_amount', 'band')
    ordering = ['position']
