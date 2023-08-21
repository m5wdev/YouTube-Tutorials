from django.contrib import admin

from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from apps.services.models import Services


@admin.register(Services)
# class ServicesAdmin(admin.ModelAdmin):
# class ServicesAdmin(MPTTModelAdmin):
class ServicesAdmin(DraggableMPTTAdmin):
    search_fields = ['name']