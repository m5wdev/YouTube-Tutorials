from django.db import models


class MetroLine(models.Model):
    name  = models.CharField('Название линии метро', max_length=255)
    color = models.CharField('Цвет линии', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'metro_lines'
        verbose_name = 'Линия Метро'
        verbose_name_plural = 'Метро (Линии)'
