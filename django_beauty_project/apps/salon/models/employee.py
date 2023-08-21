from django.db import models
from django.utils.html import mark_safe

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

from apps.salon.models.salon import Salon
from apps.services.models import Services


def image_upload_path(instance, filename):
    filename = filename.lower()
    return f'employee/{filename}'

class Employee(models.Model):
    active     = models.BooleanField('Активный', default=True, help_text='Опубликован на сайте?')
    salon      = models.ForeignKey(Salon, verbose_name='Салон', on_delete=models.SET_NULL, null=True)

    image      = ProcessedImageField(upload_to=image_upload_path,
                                        processors=[ResizeToFill(1280, 768)],
                                        format='JPEG',
                                        options={'quality': 75},
                                        blank=True, null=True)

    surname    = models.CharField('Фамилия', max_length=255)
    name       = models.CharField('Имя', max_length=255)
    patronymic = models.CharField('Отчество', max_length=255, blank=True, null=True)

    phone      = models.CharField('Телефон', max_length=60, blank=True, null=True)

    services   = models.ManyToManyField(Services, blank=True, verbose_name='Услуги')

    created    = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        if self.patronymic:
            return f'{self.surname} {self.name} {self.patronymic}'
        else:
            return f'{self.surname} {self.name}'

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'


    def get_employee_full_name(self):
        if self.patronymic:
            return f'{self.surname} {self.name} {self.patronymic}'
        else:
            return f'{self.surname} {self.name}'

    # Thumbnails
    def image_admin_thumb(self):
        return mark_safe(f'<img src="{self.image.url}" alt="" style="width: 386px; height: auto;" />')
    image_admin_thumb.short_description = 'Изображение (thumbnail)'
    # END Thumbnails