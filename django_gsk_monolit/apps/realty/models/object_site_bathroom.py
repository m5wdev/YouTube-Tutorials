from django.db import models

from apps.realty.models.object_site import ObjectSite
from apps.realty.models.object_commercial_site import ObjectCommercialSite


class ObjectBathroom(models.Model):
    BATHROOM_TYPES = (
        ('0', 'Совмещенный'),
        ('1', 'Раздельный'),
        ('2', 'На этаже'),
        ('3', 'В помещении'),
    )

    object_site   = models.ForeignKey(ObjectSite, on_delete=models.CASCADE, blank=True, null=True)
    object_commercial_site = models.ForeignKey(ObjectCommercialSite, on_delete=models.CASCADE, blank=True, null=True)

    bathroom_type = models.CharField('Тип санузла', max_length=100, choices=BATHROOM_TYPES, blank=True, null=True)
    bathroom_qty  = models.PositiveIntegerField('Количество санузлов', default=1, blank=True, null=True)

    def __str__(self):
        return self.get_bathroom_type_display()

    class Meta:
        verbose_name = 'Санузел'
        verbose_name_plural = 'Санузлы'
