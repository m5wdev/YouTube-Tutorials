from django.db import models


class ObjectCities(models.Model):
    name = models.CharField('Название города', unique=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
