from django.db import models

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from apps.core.classes.clean_media import CleanMedia
from apps.core.classes.file_processing import FileProcessing
from apps.core.classes.image_optimizer import ImageOptimizer

from apps.realty.models.object import Object
from apps.realty.models.object_commercial import ObjectCommercial


class ObjectGallery(models.Model):
    object            = models.ForeignKey(Object, verbose_name='Жилой Объект', on_delete=models.CASCADE, blank=True, null=True)
    object_commercial = models.ForeignKey(ObjectCommercial, verbose_name='Коммерческий Объект', on_delete=models.CASCADE, blank=True, null=True)

    order   = models.PositiveIntegerField('Порядок', default=0, blank=True, null=True, help_text='Чем выше число, тем ниже объект в списке')
    name    = models.CharField('Заголовок галереи', max_length=255)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Галерея Объекта'
        verbose_name_plural = 'Галереи Объектов'


def image_upload_path(instance, filename):
    object_crm_id = instance.gallery.object.crm_id
    gallery_name = instance.gallery.id

    filename = FileProcessing(filename)
    # filename = filename.newFileNameTranslitSlugify()
    filename = filename.newFileNameGenerated()
    return 'objects/{object_crm_id}/galleries/{gallery_name}/{filename}'.format(object_crm_id=object_crm_id, gallery_name=gallery_name, filename=filename)

class ObjectGalleryImage(models.Model):
    gallery     = models.ForeignKey(ObjectGallery, verbose_name='Галерея', on_delete=models.CASCADE)
    image       = models.ImageField('Изображение', upload_to=image_upload_path)
    image_thumb = ImageSpecField(source='image', processors=[ResizeToFit(256, 256)], options={'quality': 70})

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


@receiver(pre_save, sender=ObjectGallery)
def change_gallery_title(sender, instance, **kwargs):
    # titling Gallery title
    instance.name = instance.name.title()


@receiver(post_save, sender=ObjectGalleryImage)
def image_optimization(sender, instance, created, **kwargs):
    if instance.image:
        image = ImageOptimizer(instance.image.path)
        image.optimizeAndSaveImg()


@receiver(post_delete, sender=ObjectGalleryImage)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete imagekit chache file
    cleanMedia.cleanImagekitCacheImage(instance.image_thumb)
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
