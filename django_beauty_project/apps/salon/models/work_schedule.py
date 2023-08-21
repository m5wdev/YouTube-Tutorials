from django.db import models

# from apps.salon.models.salon import Salon
from apps.salon.models.address import Address


class WorkSchedule(models.Model):
    WEEK_DAYS = (
        ('0', 'Понедельник'),
        ('1', 'Вторник'),
        ('2', 'Среда'),
        ('3', 'Четверг'),
        ('4', 'Пятница'),
        ('5', 'Суббота'),
        ('6', 'Воскресенье'),
    )

    address            = models.ForeignKey(Address, verbose_name='Адрес', on_delete=models.CASCADE)
    week_day           = models.CharField('День недели', max_length=50, choices=WEEK_DAYS, blank=True, null=True)
    working_hours_from = models.TimeField('с', default='09:00')
    working_hours_to   = models.TimeField('до', default='19:00')

    def __str__(self):
        return f'{self.address} | {self.get_week_day_display()} С {self.working_hours_from} ДО {self.working_hours_to}'

    class Meta:
        verbose_name = 'График работы'
        verbose_name_plural = 'График работы'