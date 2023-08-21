from django.db import models

from django.db.models import Sum

from apps.account.models import Account
# from apps.services.models import Services

from apps.salon.models.salon_services import SalonServices
from apps.salon.models.salon import Salon
from apps.salon.models.employee import Employee


STATUSES = (
    ("cancelled", "Отменен"),
    ("done", "Исполнено"),
    ("in_progress", "В процессе"),
    ("sign_up", "Запись"),
)

class ClientAppointment(models.Model):
    client   = models.ForeignKey(Account, verbose_name='Клиент', on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee, verbose_name='Мастер', on_delete=models.SET_NULL, null=True)
    services = models.ManyToManyField(SalonServices, verbose_name='Услуги', blank=True)
    datetime = models.DateTimeField('Дата и время записи', blank=True, null=True)
    comment  = models.TextField('Комментарий', blank=True, null=True)

    status   = models.CharField('Статус', max_length=50, blank=True, null=True, choices=STATUSES)

    created  = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.client.first_name

    class Meta:
        verbose_name = 'Запись Клиента'
        verbose_name_plural = 'Записи Клиентов'

    def get_client_name(self):
        return self.client.first_name

    def get_salon_name(self):
        return self.employee.salon.name

    def calculate_total_services_price(self):
        return self.services.aggregate(total=Sum('price'))['total']