from django.contrib import admin
from .models import CategoryService, Service


@admin.register(CategoryService)
class CategoryServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category']
    ordering = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'price_max', 'category', 'company',]
    search_fields = ['name']
    list_filter = ('category',)
