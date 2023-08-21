import os, uuid

from django.db import models
from django.utils.html import mark_safe

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from .company import Company


def company_image_upload(instance, filename):
    name, ext = os.path.splitext(filename.lower())
    new_name = f'{uuid.uuid4()}{ext}'
    if instance.company.id:
        # return f'companies/{instance.company.id}/{new_name}'
        return f'companies/{instance.company.city.subdomain.name}/{instance.company.slug}/{new_name}'

class CompanyImage(models.Model):
    company = models.ForeignKey(Company,related_name='images', on_delete=models.CASCADE, verbose_name='Компания')
    image   = ProcessedImageField(verbose_name='Изображение',
                                    upload_to=company_image_upload,
                                    processors=[ResizeToFit(1920, 1080)],
                                    format='JPEG',
                                    options={'quality': 70},
                                    blank=True, null=True)

    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.image_thumbnail:
            self.image = self.image

    # Thumbnails
    def image_thumb(self):
        return mark_safe(f' \
                            <a href="{self.image_thumbnail.url}" target="_blank"> \
                                <img  src="{self.image_thumbnail.url}" alt=""> \
                            </a> \
                        ')
    image_thumb.short_description = 'Изображение'
    # END Thumbnails

    def __str__(self):
        return self.company.name

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

    class Meta:
        db_table = 'companies_images'
        verbose_name = 'Компания Изображение'
        verbose_name_plural = 'Компании Изображения'
