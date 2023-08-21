from django.db import models

from apps.realty.models.object import Object
from apps.realty.models.object_commercial import ObjectCommercial


class ObjectBlock(models.Model):
    object            = models.ForeignKey(Object, verbose_name='Жилой Объект', on_delete=models.CASCADE, blank=True, null=True)
    object_commercial = models.ForeignKey(ObjectCommercial, verbose_name='Коммерческий Объект', on_delete=models.CASCADE, blank=True, null=True)
    name              = models.CharField('Название блока', max_length=255, blank=True, null=True)

    def __str__(self):
        if self.object and not self.object_commercial:
            return f'(Жил.) {self.object} | {self.name}'
        if not self.object and self.object_commercial:
            return f'(Комм.) {self.object_commercial} | {self.name}'
        if self.object and self.object_commercial:
            return f'(Жил.) {self.object} | (Комм.) {self.object_commercial} | {self.name}'
        if not self.object and not self.object_commercial:
            return f'{self.name}'

    class Meta:
        verbose_name = 'Блок Объекта'
        verbose_name_plural = '3. Блоки Объектов'
