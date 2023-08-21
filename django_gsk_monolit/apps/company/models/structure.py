from django.db import models
from django.utils.html import mark_safe

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from ckeditor.fields import RichTextField

from apps.core.classes.clean_media import CleanMedia
from apps.core.classes.file_processing import FileProcessing
from apps.core.classes.image_optimizer import ImageOptimizer


def image_upload_path(instance, filename):
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenerated()
    return 'company/structure/{filename}'.format(filename=filename)

class Structure(models.Model):
    url   = models.URLField('URL сайта', max_length=255, blank=True, null=True)
    body  = RichTextField('Описание', blank=True, null=True)
    image = models.ImageField('Изображение', upload_to=image_upload_path, blank=True, null=True)
    order = models.PositiveIntegerField('Порядок', default=0, help_text='Чем выше число, тем ниже объект в списке')

    # Thumbnails for admin
    def image_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image.url))
    image_thumb.short_description = 'Изображение (thumbnail)'
    # END Thumbnails for admin

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'Блок (Структура компании)'
        verbose_name_plural = 'Структура компании (Блоки)'


@receiver(post_save, sender=Structure)
def image_optimization(sender, instance, created, **kwargs):
    if instance.image:
        image = ImageOptimizer(instance.image.path)
        image.optimizeAndSaveImg()


@receiver(post_delete, sender=Structure)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
