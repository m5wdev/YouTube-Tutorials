import os

from django.db import models
from django.utils.html import mark_safe

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from .category import Category


def brand_logo_upload(instance, filename):
    name, ext = os.path.splitext(filename.lower())
    new_name = f'{instance.slug}{ext}'
    if instance.slug:
        return f'brands/{instance.slug}/{new_name}'

class Brand(models.Model):
    name = models.CharField('Название бренда', max_length=255, db_index=True)
    slug = models.SlugField('Slug', unique=True, max_length=255)
    logo = ProcessedImageField(verbose_name='Логотип',
                                upload_to=brand_logo_upload,
                                # processors=[ResizeToFill(512, 512)],
                                processors=[ResizeToFit(512, 512)],
                                format='JPEG',
                                options={'quality': 75},
                                blank=True, null=True)
    categories = models.ManyToManyField(Category,related_name='brands', verbose_name='Категории', blank=True)
    popular = models.BooleanField('Популярный бренд',default=False)
    # Thumbnails
    def logo_thumb(self):
        return mark_safe(f' \
                            <a href="{self.logo.url}" target="_blank"> \
                                <img style="width: 256px; height: auto;" src="{self.logo.url}" alt=""> \
                            </a> \
                        ')
    logo_thumb.short_description = 'Превью логотипа'
    # END Thumbnails
    @property
    def first_letter( self ):
        return self.name[:1]

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'brands'
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ('name',)
