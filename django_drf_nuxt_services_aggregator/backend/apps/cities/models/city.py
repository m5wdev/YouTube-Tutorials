from django.db import models

from .subdomain import Subdomain


class City(models.Model):
    name           = models.CharField('Город', max_length=255, unique=True, help_text='e.g: Москва')
    declension_p   = models.CharField('Находится в', max_length=255, blank=True, null=True, help_text='e.g: Москве')
    declension_r   = models.CharField('Работает из', max_length=255, blank=True, null=True, help_text='e.g: Москвы')
    v_declension_p = models.CharField('Находится где', max_length=255, blank=True, null=True, help_text='e.g: в Москве')

    lower_latitude  = models.CharField('Нижняя широта', max_length=150, blank=True, null=True)
    lower_longitude = models.CharField('Нижняя долгота', max_length=150, blank=True, null=True)
    upper_latitude  = models.CharField('Верхняя широта', max_length=150, blank=True, null=True)
    upper_longitude = models.CharField('Верхняя долгота', max_length=150, blank=True, null=True)

    subdomain       = models.ForeignKey(Subdomain, verbose_name='Поддомен', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cities'
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
