from django.db import models

from apps.salon.models.salon import Salon


class City(models.Model):
    name = models.CharField('Город', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Адреса: Города'


class Metro(models.Model):
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE)
    name = models.CharField('Станция метро', max_length=255)

    def __str__(self):
        return f'{self.city}: {self.name}'

    class Meta:
        verbose_name = 'Метро'
        verbose_name_plural = 'Адреса: Станции метро'


class Address(models.Model):
    salon     = models.ForeignKey(Salon, verbose_name='Салон', on_delete=models.CASCADE)
    city      = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE)
    metro     = models.ForeignKey(Metro, verbose_name='Метро', blank=True, on_delete=models.CASCADE)
    street    = models.CharField('Улица', max_length=255, blank=True, null=True)
    building  = models.CharField('Номер дома', max_length=255, blank=True, null=True)

    latitude  = models.CharField('Широта', max_length=100, blank=True, null=True)
    longitude = models.CharField('Долгота', max_length=100, blank=True, null=True)

    def __str__(self):
        if self.metro:
            return f'{self.city}, ст.м. {self.metro.name}, {self.street} {self.building}'
        else:
            return f'{self.city}, {self.street} {self.building}'

    def display_address(self):
        return f"г. {self.city}, {self.street}, {self.building}"

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'