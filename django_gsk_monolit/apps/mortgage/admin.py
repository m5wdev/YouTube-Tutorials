from django.contrib import admin

# Admin ManyToManyField with checkboxes
from django.db import models
from django.forms import CheckboxSelectMultiple
# END Admin ManyToManyField with checkboxes

from apps.core.classes.turn_off_admin_logging import TurnOffAdminLogging
# from apps.core.classes.hide_from_admin_index import HideFromAdminIndex
from apps.core.classes.singleton_model import SingletonAdminModel

from apps.mortgage.models import Bank, Offer, WayToBuy


@admin.register(Bank)
class BankAdmin(TurnOffAdminLogging, admin.ModelAdmin):
    readonly_fields=('logo_admin_thumb',)
    fieldsets = (
        (None, {
            'fields': ('name',),
        }),
        ('Лого', {
            'fields': ('logo_admin_thumb', 'logo')
        }),
    )
    search_fields = ['name']


@admin.register(Offer)
class OfferAdmin(TurnOffAdminLogging, admin.ModelAdmin):
    # Admin ManyToManyField with checkboxes
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    # END Admin ManyToManyField with checkboxes

    list_display = ('title', 'bank')
    description_text = 'Если надо заполнить без ОТ и ДО, то заполняем оба поля одинаковыми значениями'
    fieldsets = (
        (None, {
            'fields': ('bank', 'title', 'description', 'object'),
        }),
        ('Проецентная ставка %', {
            'fields': (
                ('rate_from', 'rate_to'),
            ),
            'description': description_text
        }),
        ('Срок кредита (лет)', {
            'fields': (
                ('loan_term_from', 'loan_term_to'),
            ),
            'description': description_text
        }),
        ('Первоначальный взнос %', {
            'fields': (
                ('first_payment_from', 'first_payment_to'),
            ),
            'description': description_text
        }),
    )
    autocomplete_fields = ['bank']


@admin.register(WayToBuy)
# class WayToBuyAdmin(TurnOffAdminLogging, admin.ModelAdmin):
class WayToBuyAdmin(SingletonAdminModel, admin.ModelAdmin):
    # Admin ManyToManyField with checkboxes
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    # END Admin ManyToManyField with checkboxes
