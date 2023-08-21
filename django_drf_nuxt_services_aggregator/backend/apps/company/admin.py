from django.contrib import admin

from .models.company import Company
from .models.company_image import CompanyImage
from .models.brand import Brand
from .models.category import Category
from .models.point import Point
from .models.often_repair import OftenRepair

from apps.services.models import Service


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0

    verbose_name = "Услуга компании"
    verbose_name_plural = "Услуги компании"


class CompanyImageInline(admin.TabularInline):
    model = CompanyImage
    extra = 0
    max_num = 50

    readonly_fields = ('image_thumb','image_thumbnail')
    fields = ('image', 'image_thumb','image_thumbnail')

    verbose_name = "Изображение компании"
    verbose_name_plural = "Изображения компании"


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [
        CompanyImageInline,
        ServiceInline,
    ]

    list_display = ('name', 'city', 'is_promo', 'promo', 'updated')
    list_editable = ('is_promo', 'promo',)
    search_fields = ['name', 'city__name']
    readonly_fields = ('logo_thumb',)
    autocomplete_fields = ['city', 'brands', 'categories', 'points', 'often_repair']
    list_filter = ('city',)
    ordering = ('-updated',)

    fieldsets = (
        (None, {
            'fields': ('active', 'name', 'slug', 'body')
        }),
        (None, {
            'fields': ('city', 'brands', 'categories')
        }),
        ('Контактыные данные компании', {
            'fields': ('phone', 'email', 'url')
        }),
        ('Мастерские', {
            'fields': ('points',)
        }),
        ('Часто ремонтируем', {
            'fields': ('often_repair',)
        }),
        ('Параметры компании', {
            'fields': ('number_of_employees', 'year_of_foundation')
        }),
        ('Лого', {
            'fields': ('logo_thumb', 'logo')
        }),
        ('Опции компании', {
            'fields': (
                'courier_departure',
                'master_departure',
                'free_diagnostics',
                'quick_repair',
                'pay_after_repair',
                'own_warehouse',
                'free_parking',
                'fix_price',
                'cash_pay',
                'card_pay',
                'owner_register',
            )
        }),
        ('Цены', {
            'fields': ('min_price', 'max_price')
        }),
        ('Promo', {
            'fields': ('is_promo', 'promo')
        }),
        ('Яндекс инфо', {
            'fields': ('ya_id', 'ya_categories', 'ya_services')
        }),
        (None, {
            'fields': ('author',)
        }),
    )

    # Autoselect current user in admin form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user
        return form


@admin.register(CompanyImage)
class CompanyImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ['address_with_city', 'phone']
    search_fields = ['address', 'address_with_city', 'phone']
    autocomplete_fields = ['city', 'metro']

    fieldsets = (
        (None, {
            'fields': ('active', 'name',)
        }),
        ('Контактыные данные компании', {
            'fields': (
                'phone', 'office', 'address', 'address_with_city',
                'city', 'metro'
            )
        }),
        ('Время работы', {
            'fields': ('work_time',)
        }),
        ('Координаты', {
            'fields': ('latitude', 'longitude',)
        }),
        ('Модерация', {
            'fields': ('moderated',)
        }),
        (None, {
            'fields': ('author',)
        }),
    )

    # Autoselect current user in admin form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user
        return form


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    readonly_fields = ('logo_thumb',)
    search_fields = ['name']
    list_filter = ('popular',)
    autocomplete_fields = ['categories']

    fieldsets = (
        (None, {
            'fields': ('name', 'slug','popular',)
        }),

        (None, {
            'fields': ('categories',)
        }),
        (None, {
            'fields': ('logo_thumb', 'logo')
        }),
    )


class ParentCategoriesListFilter(admin.SimpleListFilter):
    title = 'Категории верхнего уровня'
    parameter_name = 'parent_category'

    def lookups(self, request, model_admin):
        list_tuple = []
        for category in Category.objects.all():
            try:
                list_tuple.append((category.parent_category.id, category.parent_category.name))
            except:
                pass
        list_tuple = list(set(list_tuple))
        list_tuple.sort(key=lambda y: y[1]) # sort by name
        return list_tuple

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent_category__id=self.value())
        else:
            return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('logo_thumb',)
    search_fields = ['name']
    list_display = ['name', 'parent_category']
    list_filter = (ParentCategoriesListFilter,)
    ordering = ['name']

    fieldsets = (
        (None, {
            'fields': ('name', 'declension_one_p', 'slug')
        }),
        (None, {
            'fields': ('parent_category',)
        }),
        (None, {
            'fields': ('logo_thumb', 'logo')
        }),
    )


@admin.register(OftenRepair)
class OftenRepairAdmin(admin.ModelAdmin):
    search_fields = ['name']
