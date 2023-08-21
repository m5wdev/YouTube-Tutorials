from django.db import models

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from django.urls import reverse
from django.utils.html import mark_safe

from ckeditor.fields import RichTextField

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

from apps.core.classes.clean_media import CleanMedia
from apps.core.classes.file_processing import FileProcessing
from apps.core.classes.image_optimizer import ImageOptimizer

from apps.realty.models.object_types import ObjectTypes
from apps.realty.models.object_building_types import ObjectBuildingTypes
from apps.realty.models.object_cities import ObjectCities


def genplan_upload_path(instance, filename):
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenplan()
    return f'objects-commercial/{instance.crm_id}/{filename}'

def image_upload_path(instance, filename):
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenerated()
    return f'objects-commercial/{instance.crm_id}/images/{filename}'

def slider_image_upload(instance, filename):
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenerated()
    return f'objects-commercial/{instance.crm_id}/slider/{filename}'

class ObjectCommercial(models.Model):
    active        = models.BooleanField('Активный', default=True, help_text='Опубликован на сайте')
    completed     = models.BooleanField('Объект сдан', default=False)
    all_sold      = models.BooleanField('Все помещения проданы', default=False, help_text='Все квартиры и помещения проданы')

    order         = models.PositiveIntegerField('Порядок', default=0, blank=True, null=True, help_text='Чем выше число, тем ниже объект в списке')
    crm_id        = models.CharField('CRM ID', max_length=100, unique=True, help_text='ID объекта в 1C (Заполняется автоматически при выгрузке)')

    name          = models.CharField('Название объекта', unique=True, max_length=255, db_index=True)
    slug          = models.SlugField('URL адрес', max_length=100, unique=True, help_text='e.g.: status-house (max 100 chars), получим https://monolit.site/commercial/status-house/')

    object_type   = models.ForeignKey(ObjectTypes, verbose_name='Тип Объекта', on_delete=models.SET_NULL, blank=True, null=True)
    building_type = models.ForeignKey(ObjectBuildingTypes, verbose_name='Тип Здания', on_delete=models.SET_NULL, blank=True, null=True)
    description   = RichTextField('Описание', blank=True, null=True)

    city          = models.ForeignKey(ObjectCities, verbose_name='Город', on_delete=models.SET_NULL, blank=True, null=True)
    address       = models.CharField('Адрес', max_length=255, blank=True, null=True, help_text='Улица, номер дома')

    genplan       = models.ImageField('Генплан', upload_to=genplan_upload_path, blank=True, null=True, help_text='Изображение с генпланом')
    genplan_svg   = models.TextField('SVG объекты на генплане', blank=True, null=True)

    main_image       = models.ImageField('Главное изображение', upload_to=image_upload_path, blank=True, null=True)
    main_image_thumb = ImageSpecField(source='main_image', processors=[ResizeToFill(512, 386)], format = 'JPEG', options={'quality': 70})

    # Slider
    slider_main_image = ProcessedImageField(verbose_name='Изображение для слайдера',
                                            upload_to=slider_image_upload,
                                            processors=[ResizeToFill(1920, 600)],
                                            format='JPEG',
                                            options={'quality': 70},
                                            blank=True, null=True,
                                        )

    webcam        = models.URLField('Cсылка на web-камеру', blank=True, null=True, help_text='e.g.: https://rtsp.me/embed/3KASrTkG/')
    panoram       = models.URLField('Cсылка на панораму', blank=True, null=True, help_text='e.g.: https://monolit360.com/files/main/index.html?s=pano1692')

    updated       = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)

    # Thumbnails for admin
    def genplan_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.genplan.url))
    genplan_thumb.short_description = 'Генплан (thumbnail)'

    def main_image_thumb_admin(self):
        return mark_safe('<img src="{}" alt="" style="width: 40%; height: auto;" />'.format(self.main_image.url))
    main_image_thumb_admin.short_description = 'Главное изображение (thumbnail)'

    def slider_main_image_thumb_admin(self):
        return mark_safe('<img src="{}" alt="" style="width: 40%; height: auto;" />'.format(self.slider_main_image.url))
    slider_main_image_thumb_admin.short_description = 'Изображение для слайдера (thumbnail)'
    # END Thumbnails for admin

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('objects-commercial:detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Коммерческий Объект'
        verbose_name_plural = '2. Коммерческие Объекты'

    def display_name(self):
        return f'{self.object_type} {self.name}'


@receiver(post_save, sender=ObjectCommercial)
def images_optimization(sender, instance, created, **kwargs):
    if instance.genplan:
        image = ImageOptimizer(instance.genplan.path)
        image.optimizeAndSaveImg()
    if instance.main_image:
        image = ImageOptimizer(instance.main_image.path)
        image.optimizeAndSaveImg()


@receiver(post_delete, sender=ObjectCommercial)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete imagekit chache file
    cleanMedia.cleanImagekitCacheImage(instance.main_image_thumb)
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
