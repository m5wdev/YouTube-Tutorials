from django.db import models
from apps.realty.models.object_site import ObjectSite


class ObjectBalcony(models.Model):
    BALCONY_TYPES = (
        ('balcony', 'Балкон'),
        ('loggia', 'Лоджия'),
        ('terrace', 'Терраса'),
        ('patio', 'Патио'),
        ('french_balcony', 'Французский балкон'),
        ('bay_window', 'Эркер'),
    )

    object_site  = models.ForeignKey(ObjectSite, on_delete=models.CASCADE, blank=True, null=True)
    balcony_type = models.CharField('Тип балкона', max_length=100, choices=BALCONY_TYPES, blank=True, null=True)
    balcony_qty  = models.PositiveIntegerField('Количество балконов', default=1, blank=True, null=True)

    def __str__(self):
        return self.get_balcony_type_display()

    class Meta:
        verbose_name = 'Балкон'
        verbose_name_plural = 'Балконы в помещении'
