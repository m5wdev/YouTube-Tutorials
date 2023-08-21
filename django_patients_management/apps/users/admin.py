from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from apps.users.models import CustomUser, DoctorWorkSchedule
from apps.users.forms import CustomUserCreationForm, CustomUserChangeForm


class DoctorWorkScheduleInline(admin.TabularInline):
    model = DoctorWorkSchedule
    extra = 1
    fk_name = 'doctor'
    # max_num = 7

    # Get only doctors in admin foreign key
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            kwargs["queryset"] = CustomUser.objects.filter(groups__name__in=['Врач',])
        if db_field.name == "patient":
            kwargs["queryset"] = CustomUser.objects.filter(groups__name__in=['Пациент',])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = []

    model = CustomUser
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm

    list_display = ['username', 'fio', 'email', 'gender', 'birth_date', 'user_groups_display', 'is_staff']

    # Add user
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'fio',
                    'gender',
                    'birth_date',
                    'groups',
                )
            }
        )
    )

    # Edit user
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'fio',
                    'gender',
                    'birth_date',
                )
            }
        )
    )

    def user_groups_display(self, user):
        try:
            groups = []
            for group in user.groups.all():
                groups.append(group.name)
            return ', '.join(groups)
        except:
            return '-'

    def get_inlines(self, request, obj):
        if obj is not None:
            print(obj)
            # if user in Врач group, display inline form
            if obj.groups.filter(name='Врач').exists():
                return [DoctorWorkScheduleInline]
        return []

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     # if user in Врач group, display inline form
    #     # if obj.groups.filter(name='Врач').exists():
    #     #     pass
    #     return form

# admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(DoctorWorkSchedule)
class DoctorWorkScheduleAdmin(admin.ModelAdmin):
    # Get only doctors in admin foreign key
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            kwargs["queryset"] = CustomUser.objects.filter(groups__name__in=['Врач',])
        if db_field.name == "patient":
            kwargs["queryset"] = CustomUser.objects.filter(groups__name__in=['Пациент',])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
