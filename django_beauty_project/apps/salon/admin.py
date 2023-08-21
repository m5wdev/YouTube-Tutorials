from django.contrib import admin

from apps.salon.models.salon import Salon
from apps.salon.models.salon_services import SalonServices
from apps.salon.models.employee import Employee
from apps.salon.models.client import Client
from apps.salon.models.work_schedule import WorkSchedule
from apps.salon.models.client_appointment import ClientAppointment
from apps.salon.models.address import City, Metro, Address


class WorkScheduleInline(admin.TabularInline):
    model = WorkSchedule
    extra = 7
    max_num = 7


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    max_num = 10


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline,
    ]

    fieldsets = (
        (None, {
            'fields': ('active', 'name', 'description')
        }),
        ('Контакты салона', {
            'fields': ('phone', 'email', 'site_url')
        }),
    )

    search_fields = ['name']


@admin.register(SalonServices)
class SalonServicesAdmin(admin.ModelAdmin):
    search_fields = ['service']
    autocomplete_fields = ['salon',]

    list_display = ('service', 'price', 'salon',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ('image_admin_thumb',)
    # list_display = ('surname', 'name', 'patronymic', 'salon',)
    list_display = ('__str__', 'salon',)

    fieldsets = (
        (None, {
            'fields': ('active',)
        }),
        ('ФИО', {
            'fields': ('surname', 'name', 'patronymic')
        }),
        ('Контакты сотрудника', {
            'fields': ('phone',)
        }),
        ('Фото сотрудника', {
            'fields': ('image_admin_thumb', 'image')
        }),
        ('Салон\Услуги', {
            'fields': ('salon', 'services',)
        }),
    )

    search_fields = ['__str__']
    autocomplete_fields = ['salon', 'services']


@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('address',)
        }),
        ('График работы', {
            'fields': ('week_day', 'working_hours_from', 'working_hours_to',)
        }),
    )

    # autocomplete_fields = ['salon',]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    autocomplete_fields = ['salon',]


@admin.register(ClientAppointment)
class ClientAppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_client_name', 'client', 'get_salon_name', 'employee', 'datetime', 'status')
    autocomplete_fields = ['client', 'employee', 'services']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    # search_fields = ['name']
    pass


@admin.register(Metro)
class MetroAdmin(admin.ModelAdmin):
    # search_fields = ['name']
    # autocomplete_fields = ['city',]
    ordering = ('name',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    inlines = [
        WorkScheduleInline,
    ]

    list_display = ('salon', 'city', 'metro', 'street', 'building')
    # autocomplete_fields = ['city', 'metro',]
    # autocomplete_fields = ['city_name', 'metro_name',]