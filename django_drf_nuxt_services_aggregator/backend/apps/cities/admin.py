from django.contrib import admin

from .models.city import City
from .models.subdomain import Subdomain

from .models.metro_line import MetroLine
from .models.metro_station import MetroStation


@admin.register(Subdomain)
class SubdomainAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['subdomain']
    list_display = ['name', 'subdomain']

    fieldsets = (
        ('Имя и склонения', {
            'fields': ('name', 'declension_p', 'declension_r', 'v_declension_p')
        }),
        ('Поддомен', {
            'fields': ('subdomain',)
        }),
        ('Широта\Долгота Верх', {
            'fields': ('upper_latitude', 'upper_longitude',)
        }),
        ('Широта\Долгота Низ', {
            'fields': ('lower_latitude', 'lower_longitude',)
        }),
    )
    ordering = ('name',)


@admin.register(MetroLine)
class MetroLineAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'color']


class CitiesWithMetroListFilter(admin.SimpleListFilter):
    title = 'Города с метро'
    parameter_name = 'cities_metro'

    def lookups(self, request, model_admin):
        list_tuple = []
        for city in MetroStation.objects.all():
            list_tuple.append((city.city.id, city.city.name))
        list_tuple = list(set(list_tuple))
        list_tuple.sort(key=lambda y: y[1]) # sort by city_name
        return list_tuple

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(city__id=self.value())
        else:
            return queryset


@admin.register(MetroStation)
class MetroStationAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['city', 'metro_line']
    list_display = ['name', 'metro_line', 'city']
    # list_filter = ('city',)
    list_filter = (CitiesWithMetroListFilter,)
