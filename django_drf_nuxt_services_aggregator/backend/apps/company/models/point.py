from django.db import models

from apps.users.models import CustomUser
from apps.cities.models.city import City
from apps.cities.models.metro_station import MetroStation
# from apps.company.models.company import Company


class Point(models.Model):
    active = models.BooleanField('Активная', default=True)
    name   = models.CharField('Название мастерской', max_length=255, blank=True, null=True)

    phone   = models.CharField('Телефон', max_length=255, blank=True, null=True)
    office  = models.CharField('Офис', max_length=255, blank=True, null=True)
    address = models.CharField('Адрес', max_length=255, blank=True, null=True)
    address_with_city = models.CharField('Адрес (с городом)', max_length=255, blank=True, null=True)

    work_time   = models.TextField('Время работы', blank=True, null=True)

    latitude  = models.CharField('Широта', max_length=255, blank=True, null=True)
    longitude = models.CharField('Долгота', max_length=255, blank=True, null=True)

    city  = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE, blank=True, null=True)
    metro = models.ManyToManyField(MetroStation, verbose_name='Станции метро', blank=True)

    moderated = models.BooleanField('Модерированно', default=False)
    author    = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Автор')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.address_with_city:
            try:
                self.address_with_city = self.city + ', '+self.address
            except:
                pass

    def __str__(self):
        return self.address_with_city or 'no address'

    def get_city_name(self):
        return self.city

    def get_author_name(self):
        return self.author.name

    class Meta:
        db_table = 'company_points'
        verbose_name = 'Мастерская'
        verbose_name_plural = 'Мастерские'
