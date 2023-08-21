from django.contrib import admin

from .models.company_application import CompanyApplication
from .models.company_abuse import CompanyAbuse
from .models.repair_application import RepairApplication


@admin.register(CompanyApplication)
class CompanyApplicationAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'name', 'company_name')


@admin.register(CompanyAbuse)
class CompanyAbuseAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'company_name', 'abuse_type', 'description')


@admin.register(RepairApplication)
class RepairApplicationAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'name', 'phone', 'issue_type')
