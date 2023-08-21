from django.contrib import admin

from apps.core.classes.turn_off_admin_logging import TurnOffAdminLogging

from apps.pages.models import Pages


@admin.register(Pages)
class PagesAdmin(TurnOffAdminLogging, admin.ModelAdmin):
    pass
