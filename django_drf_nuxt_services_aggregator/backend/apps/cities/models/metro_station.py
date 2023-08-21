from django.db import models

from .city import City
from .metro_line import MetroLine


class MetroStation(models.Model):
    name       = models.CharField('Название станции метро', max_length=255)
    metro_line = models.ForeignKey(MetroLine,related_name='station_metro', on_delete=models.CASCADE, verbose_name='Линия метро')
    city       = models.ForeignKey(City,related_name='station_metro', on_delete=models.CASCADE, verbose_name='Город')

    def __str__(self):
        return self.name

    def get_metro_line_name(self):
        return self.metro_line

    def get_city_name(self):
        return self.city

    class Meta:
        db_table = 'metro_stations'
        verbose_name = 'Станция Метро'
        verbose_name_plural = 'Метро (Станции)'
