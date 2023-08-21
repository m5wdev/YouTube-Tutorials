from django.db import models
from django.utils.html import mark_safe

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from apps.core.classes.clean_media import CleanMedia
from apps.core.classes.file_processing import FileProcessing
from apps.core.classes.image_optimizer import ImageOptimizer


def image_upload_path(instance, filename):
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenerated()
    return 'company/certificates/{filename}'.format(filename=filename)

class Certificate(models.Model):
    title = models.CharField('Название сертификата', max_length=100)
    image = models.ImageField('Фото сертификата', upload_to=image_upload_path, blank=True, null=True)

    # Thumbnails for admin
    def image_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image.url))
    image_thumb.short_description = 'Фото сертификата (thumbnail)'
    # Thumbnails for admin

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'


@receiver(post_save, sender=Certificate)
def image_optimization(sender, instance, created, **kwargs):
    if instance.image:
        image = ImageOptimizer(instance.image.path)
        image.optimizeAndSaveImg()


@receiver(post_delete, sender=Certificate)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
