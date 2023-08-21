from django.contrib import admin

from apps.core.classes.turn_off_admin_logging import TurnOffAdminLogging
from apps.core.classes.hide_from_admin_index import HideFromAdminIndex

from apps.news.models.news import NewsCategory, News, NewsImage
from apps.news.models.actions import Actions, ActionsPartner


@admin.register(NewsCategory)
class NewsCategoryAdmin(TurnOffAdminLogging, admin.ModelAdmin):
    search_fields = ['name']


""" [ NewsImage ] """
class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 0
    max_num = 50
    readonly_fields = ('image_thumb',)

@admin.register(NewsImage)
class NewsImageAdmin(TurnOffAdminLogging, HideFromAdminIndex, admin.ModelAdmin):
    pass
""" [ END NewsImage ] """


""" [ News ] """
@admin.register(News)
class NewsAdmin(TurnOffAdminLogging, admin.ModelAdmin):
    inlines = [
        NewsImageInline,
    ]

    readonly_fields = ('main_image_admin_thumb',)
    fieldsets = (
        (None, {
            'fields': ('active', 'title', 'object', 'category', 'date', 'body')
        }),
        ('Главное изображение', {
           'fields': ('main_image_admin_thumb', 'main_image')
        }),
    )
    list_display = ('title', 'active', 'updated')
    autocomplete_fields = ['object', 'category']
""" [ END News ] """


""" [ ActionsPartner ] """
class ActionsPartnerInline(admin.TabularInline):
    model = ActionsPartner
    extra = 0
    max_num = 20
    fields = ('name', 'logo_thumb', 'logo', 'site_url')
    readonly_fields = ('logo_thumb',)

@admin.register(ActionsPartner)
class ActionsPartnerAdmin(TurnOffAdminLogging, HideFromAdminIndex, admin.ModelAdmin):
    pass
""" [ END ActionsPartner ] """


""" [ Actions ] """
@admin.register(Actions)
class ActionsAdmin(TurnOffAdminLogging, admin.ModelAdmin):
    inlines = [
        ActionsPartnerInline,
    ]

    readonly_fields = ('image_card_thumb', 'image_detail_thumb',)
    fieldsets = (
        (None, {
            'fields': ('active', 'title', 'description', 'partners_title')
        }),
        ('Даты начала и окончания', {
           'fields': ('date_start', 'date_end')
        }),
        ('Изображение для карточки', {
           'fields': ('image_card_thumb', 'image_card')
        }),
        ('Изображение для страницы', {
           'fields': ('image_detail_thumb', 'image_detail')
        }),
    )
    list_display = ('title', 'active', 'date_start', 'date_end')
""" [ END Action ] """
