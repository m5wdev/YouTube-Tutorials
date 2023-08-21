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
    return 'company/management/{filename}'.format(filename=filename)

class Management(models.Model):
    image      = models.ImageField('Фото руководителя', upload_to=image_upload_path, blank=True, null=True)
    surname    = models.CharField('Фамилия', max_length=255)
    name       = models.CharField('Имя', max_length=255)
    patronymic = models.CharField('Отчество', max_length=255, blank=True, null=True)
    position   = models.CharField('Должность', max_length=255)
    order      = models.PositiveIntegerField('Порядок', default=0, blank=True, null=True, help_text='Чем выше число, тем ниже объект в списке')


    # Thumbnails for admin
    def image_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image.url))
    image_thumb.short_description = 'Фото руководителя (thumbnail)'
    # Thumbnails for admin

    def __str__(self):
        return self.position

    class Meta:
        verbose_name = 'Менеджмент (Рукововодство)'
        verbose_name_plural = 'Менеджмент (Руководители)'


@receiver(post_save, sender=Management)
def image_optimization(sender, instance, created, **kwargs):
    if instance.image:
        image = ImageOptimizer(instance.image.path)
        image.optimizeAndSaveImg()


@receiver(post_delete, sender=Management)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
