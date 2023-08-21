from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Services(MPTTModel):
    name   = models.CharField('Название услуги', max_length=255, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children', verbose_name='Родитель')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name