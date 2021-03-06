from django.contrib import admin
from . import models
from django.utils.html import format_html


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'is_pinned')
    exclude = ('called_bet',)


@admin.register(models.Sticker)
class StickerAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_sticker')

    def show_sticker(self, obj):
        return format_html('<img src="{}" width="50"/>'.format(obj.sticker_picture.url))

    show_sticker.short_description = 'Sticker'
