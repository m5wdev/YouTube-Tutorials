from django.db import models


class ObjectBuildingTypes(models.Model):
    name = models.CharField('Тип Здания', unique=True, max_length=255)
    slug = models.CharField('Тип Здания (eng)', max_length=100, unique=True, blank=True, null=True, help_text='e.g.: если название "Монолитно-каркасный", то здесь заполняется как "monolith-frame"')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип Здания'
        verbose_name_plural = 'Типы Зданий'
