import os
import uuid

from django.db import models
from django.utils.html import mark_safe

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit


def category_logo_upload(instance, filename):
    name, ext = os.path.splitext(filename.lower())
    new_name = f'{uuid.uuid4()}{ext}'
    return f'categories/{new_name}'


class Category(models.Model):
    name = models.CharField('Название категории', db_index=True, max_length=255, help_text='e.g.: 3D-принтеры')
    slug = models.SlugField('Slug', unique=True, max_length=255)
    declension_one_p = models.CharField('Склонение', max_length=255, blank=True, null=True, help_text='e.g.: 3D-принтеров')
    logo = ProcessedImageField(verbose_name='Логотип',
                                upload_to=category_logo_upload,
                                # processors=[ResizeToFill(512, 512)],
                                processors=[ResizeToFit(512, 512)],
                                format='JPEG',
                                options={'quality': 75},
                                blank=True, null=True)
    parent_category = models.ForeignKey('self',db_index=True, verbose_name='Родительская категория', related_name='children_category', on_delete=models.CASCADE, blank=True, null=True)
    important = models.BooleanField('Важное', help_text='Отображать ли в брендах и т д', default=False)

    # Thumbnails
    def logo_thumb(self):
        return mark_safe(f' \
                            <a href="{self.logo.url}" target="_blank"> \
                                <img style="width: 256px; height: auto;" src="{self.logo.url}" alt=""> \
                            </a> \
                        ')
    logo_thumb.short_description = 'Превью логотипа'
    # END Thumbnails

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
