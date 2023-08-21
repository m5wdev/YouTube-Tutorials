from django.db import models
from apps.realty.models.object_section import ObjectSection


class ObjectElevator(models.Model):
    ELEVATORS_TYPES = (
        ('passenger_lift', 'Пассажирский лифт'),
        ('cargo_lift', 'Грузовой лифт'),
    )

    object_section = models.ForeignKey(ObjectSection, verbose_name='Секция Объекта', on_delete=models.CASCADE)
    elevator_type  = models.CharField('Тип лифта', max_length=100, choices=ELEVATORS_TYPES, blank=True, null=True)
    elevator_qty   = models.PositiveIntegerField('Количество лифтов', default=1, blank=True, null=True)

    def __str__(self):
        return self.elevator_type

    class Meta:
        verbose_name = 'Лифт Объекта'
        verbose_name_plural = 'Лифты Объекта'
