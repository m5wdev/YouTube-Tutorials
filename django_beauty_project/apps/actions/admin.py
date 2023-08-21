from django.contrib import admin
from apps.actions.models import Actions


@admin.register(Actions)
class ActionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'salon', 'action_type')
    search_fields = ['username']