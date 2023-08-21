from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

from apps.salon.models.salon import Salon
from apps.services.models import Services


def image_upload_path(instance, filename):
    filename = filename.lower()
    return f'actions/{filename}'

ACTION_TYPES = (
    ("0", "Скидка на услугу"),
    ("1", "Скидка на услуги в определенные часы/дни"),
    ("2", "Скидка на первое посещение"),
    ("3", "Подарок"),
    ("4", "Подарок за первое посещение"),
)

class Actions(models.Model):
    active      = models.BooleanField('Активный', default=True, help_text='Опубликован на сайте?')

    action_type = models.CharField('Тип акции', max_length=1, blank=True, null=True, choices=ACTION_TYPES)

    salon       = models.ForeignKey(Salon, on_delete=models.SET_NULL, null=True, verbose_name='Салон')
    services    = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True, verbose_name='Услуги')

    title       = models.CharField('Заголовок акции', max_length=255)

    image       = ProcessedImageField(upload_to=image_upload_path,
                                        processors=[ResizeToFill(1280, 768)],
                                        format='JPEG',
                                        options={'quality': 75},
                                        blank=True, null=True)

    description = models.TextField('Описание', blank=True, null=True)

    discount    = models.PositiveIntegerField('Скидка', blank=True, null=True, \
                                                validators=[MinValueValidator(1), MaxValueValidator(100)])

    created     = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
