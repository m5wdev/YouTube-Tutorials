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
    object_crm_id = instance.crm_id
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenplan()
    return f'objects/{object_crm_id}/{filename}'

def image_upload_path(instance, filename):
    object_crm_id = instance.crm_id
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenerated()
    return f'objects/{object_crm_id}/images/{filename}'

def slider_image_upload(instance, filename):
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenerated()
    return f'objects/{instance.crm_id}/slider/{filename}'

class Object(models.Model):
    active        = models.BooleanField('Активный', default=True, help_text='Опубликован на сайте')
    completed     = models.BooleanField('Объект сдан', default=False)
    all_sold      = models.BooleanField('Все помещения проданы', default=False, help_text='Все квартиры и помещения проданы')
    partnership   = models.BooleanField('Партнерская программа', default=False, help_text='Участвует ли данный объект в партнерской программе?')

    order         = models.PositiveIntegerField('Порядок', default=0, blank=True, null=True, help_text='Чем выше число, тем ниже объект в списке')
    crm_id        = models.CharField('CRM ID', max_length=100, unique=True, help_text='ID объекта в 1C (Заполняется автоматически при выгрузке)')

    name          = models.CharField('Название объекта', max_length=255, unique=True, db_index=True)
    slug          = models.SlugField('URL адрес', max_length=100, unique=True, help_text='e.g.: status-house (max 100 chars), получим https://monolit.site/objects/status-house/')

    object_type   = models.ForeignKey(ObjectTypes, verbose_name='Тип Объекта', on_delete=models.SET_NULL, blank=True, null=True)
    building_type = models.ForeignKey(ObjectBuildingTypes, verbose_name='Тип Здания', on_delete=models.SET_NULL, blank=True, null=True)
    description   = RichTextField('Описание', blank=True, null=True)

    city          = models.ForeignKey(ObjectCities, verbose_name='Город', on_delete=models.SET_NULL, blank=True, null=True)
    address       = models.CharField('Адрес', max_length=255, blank=True, null=True, help_text='Улица, номер дома')

    genplan       = models.ImageField('Генплан', upload_to=genplan_upload_path, blank=True, null=True, help_text='Изображение с генпланом')
    genplan_svg   = models.TextField('SVG объекты на генплане', blank=True, null=True)

    yandex_map    = models.TextField('Карта из Яндекса', blank=True, null=True, help_text='Создайте и карту сметками в Конструкторе Яндекс Карт https://yandex.ru/map-constructor/ и добавьте в данное поле код JavaScript код с параметром scroll=false')

    main_image       = models.ImageField('Главное изображение', upload_to=image_upload_path, blank=True, null=True)
    main_image_thumb = ImageSpecField(source='main_image', processors=[ResizeToFill(512, 386)], format = 'JPEG', options={'quality': 70})

    # Slider
    slider_main_image = ProcessedImageField(verbose_name='Изображение для слайдера на Главной',
                                            upload_to=slider_image_upload,
                                            processors=[ResizeToFill(1920, 600)],
                                            format='JPEG',
                                            options={'quality': 70},
                                            blank=True, null=True,
                                        )

    slider_completed_image = ProcessedImageField(verbose_name='Изображение для слайдера Завершенный объект',
                                            upload_to=slider_image_upload,
                                            processors=[ResizeToFill(386, 512)],
                                            format='PNG',
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
    slider_main_image_thumb_admin.short_description = 'Изображение для слайдера на Главной (thumbnail)'

    def slider_completed_image_thumb_admin(self):
        return mark_safe('<img src="{}" alt="" style="width: auto; height: auto;" />'.format(self.slider_completed_image.url))
    slider_completed_image_thumb_admin.short_description = 'Изображение для слайдера Завершенный объект (thumbnail)'
    # END Thumbnails for admin

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('objects:detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Жилой Объект'
        verbose_name_plural = '1. Жилые Объекты'

    def display_name(self):
        return f'{self.object_type} {self.name}'


@receiver(post_save, sender=Object)
def images_optimization(sender, instance, created, **kwargs):
    if instance.genplan:
        image = ImageOptimizer(instance.genplan.path)
        image.optimizeAndSaveImg()
    if instance.main_image:
        image = ImageOptimizer(instance.main_image.path)
        image.optimizeAndSaveImg()
    if instance.slider_main_image:
        image = ImageOptimizer(instance.slider_main_image.path)
        image.optimizeAndSaveImg()
    if instance.slider_completed_image:
        image = ImageOptimizer(instance.slider_completed_image.path)
        image.optimizeAndSaveImg()
    # Delete empty dirs in /media/
    # cleanMedia = CleanMedia()
    # cleanMedia.deleteEmptyDirsRecusive()


@receiver(post_delete, sender=Object)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete imagekit chache file
    cleanMedia.cleanImagekitCacheImage(instance.main_image_thumb)
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
