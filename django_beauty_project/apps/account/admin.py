from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.account.models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'email', 'phone', 'salon', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_superuser')
    search_fields = ('phone', 'username')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {
            'fields': ('username', 'phone', 'email', 'first_name', 'city', 'birth_date', 'password')
        }),
        ('Status', {
            'fields': ('is_staff', 'is_admin', 'is_superuser')
        }),
        ('Groups and Permissions', {
            'fields': ('groups', 'user_permissions')
        }),
        ('Salon', {
            'fields': ('salon',)
        }),
        ('Misc. Info', {
            'fields': ('date_joined', 'last_login')
        }),
    )

    filter_horizontal = ()
    list_filter = ()
    # fieldsets = ()

    autocomplete_fields = ['salon']