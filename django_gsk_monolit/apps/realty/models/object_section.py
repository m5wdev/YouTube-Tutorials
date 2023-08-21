import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.realty.models.object import Object
from apps.realty.models.object_block import ObjectBlock
from apps.realty.models.object_commercial import ObjectCommercial


class ObjectSection(models.Model):
    YEAR_QUARTERS = (
        ('1', '1-й Квартал'),
        ('2', '2-й Квартал'),
        ('3', '3-й Квартал'),
        ('4', '4-й Квартал'),
    )

    object            = models.ForeignKey(Object, verbose_name='Жилой Объект', on_delete=models.CASCADE, blank=True, null=True)
    object_commercial = models.ForeignKey(ObjectCommercial, verbose_name='Коммерческий Объект', on_delete=models.CASCADE, blank=True, null=True)
    object_block      = models.ForeignKey(ObjectBlock, verbose_name='Блок Объекта', on_delete=models.CASCADE, default=0, blank=True, null=True)

    name              = models.CharField('Название секции', max_length=255, help_text='Название секции и её номер. Например: Секция 1')

    comlete_quarter   = models.CharField('Квартал сдачи', max_length=10, choices=YEAR_QUARTERS, blank=True, null=True)
    comlete_year      = models.PositiveIntegerField('Год сдачи', default=datetime.date.today().year, blank=True, null=True,
                                                    validators=[MinValueValidator(2006), MaxValueValidator(2100)],
                                                    help_text='Допустимые значения от 2006 до 2100')

    floor_first       = models.IntegerField('Этаж Первый', blank=True, null=True,
                                            validators=[MinValueValidator(-5), MaxValueValidator(1)],
                                            help_text='мин. этаж: -5')
    floor_last        = models.IntegerField('Этаж Последний', blank=True, null=True,
                                            validators=[MinValueValidator(0), MaxValueValidator(100)],
                                            help_text='макс. этаж: 100')

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
        verbose_name = 'Секция Объекта'
        verbose_name_plural = '4. Секции Объектов'
