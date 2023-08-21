from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form     = CustomUserChangeForm
    model    = CustomUser

    list_display = ('id', 'username', 'email', 'email_confirmed', 'first_name', 'get_avatar_photo', 'is_staff', 'is_active')
    list_display_links = ('username','email',)
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email')
        }),
        ('Персональная информация', {
            'fields': ('first_name', 'avatar', 'email_confirmed')
        }),
        ('Права и группы', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (None, {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'avatar', 'first_name', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )

    search_fields = ('username', 'email',)
    ordering = ('id',)

    def get_avatar_photo(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="100" alt="">')
    get_avatar_photo.short_description = 'Аватар пользователя'
