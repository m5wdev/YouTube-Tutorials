from django.db import models

from mptt.fields import TreeForeignKey

from apps.salon.models.salon import Salon
from apps.salon.models.address import Address

from apps.services.models import Services


class SalonServices(models.Model):
    salon   = models.ForeignKey(Salon, verbose_name='Салон', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name='Адрес', on_delete=models.CASCADE)
    service = TreeForeignKey(Services, on_delete=models.CASCADE, verbose_name="Услуга")
    price   = models.DecimalField('Цена', max_digits=10, decimal_places=2)

    def __str__(self):
        return self.service.name

    class Meta:
        verbose_name = 'Услуга Салона'
        verbose_name_plural = 'Услуги Салонов'