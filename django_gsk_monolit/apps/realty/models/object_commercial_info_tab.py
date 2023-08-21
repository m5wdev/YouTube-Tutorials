from django.db import models
from django.utils.html import mark_safe

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from ckeditor.fields import RichTextField

from apps.core.classes.clean_media import CleanMedia
from apps.core.classes.file_processing import FileProcessing
from apps.core.classes.image_optimizer import ImageOptimizer

from apps.realty.models.object_commercial import ObjectCommercial


def image_upload_path(instance, filename):
    object_crm_id = instance.object_commercial.crm_id
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenerated()
    return f'objects-commercial/{object_crm_id}/info-tabs/{filename}'

class ObjectCommercialInfoTab(models.Model):
    ICONS = (
        ('about', 'Об объекте'),
        ('architecture', 'Архитектура'),
        ('land-improvement', 'Благоустройство'),
        ('location', 'Расположение'),
        ('communications', 'Коммуникации'),
        ('arrangement', 'Планировки'),
        ('parking', 'Паркинг'),
        ('servicing', 'Обслуживание'),
    )

    object_commercial = models.ForeignKey(ObjectCommercial, on_delete=models.CASCADE, default=0)
    icon_name         = models.SlugField('Имя иконки (оно же заголовок таба)', max_length=100, choices=ICONS, blank=True, null=True)
    description       = RichTextField('Описание', blank=True, null=True)
    image             = models.ImageField('Изображение', upload_to=image_upload_path, blank=True, null=True)

    def image_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 128px; height: auto;" />'.format(self.image.url))
    image_thumb.short_description = 'Изображение (thumbnail)'

    def __str__(self):
        return self.get_icon_name_display()

    class Meta:
        verbose_name = 'Таб [Информация о коммерческом объекте]'
        verbose_name_plural = 'Табы [Информация о коммерческих объектах]'


@receiver(post_save, sender=ObjectCommercialInfoTab)
def image_optimization(sender, instance, created, **kwargs):
    if instance.image:
        image = ImageOptimizer(instance.image.path)
        image.optimizeAndSaveImg()


@receiver(post_delete, sender=ObjectCommercialInfoTab)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
