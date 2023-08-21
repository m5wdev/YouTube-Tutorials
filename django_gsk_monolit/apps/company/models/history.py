import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models
from django.utils.html import mark_safe

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from ckeditor.fields import RichTextField

from apps.core.classes.clean_media import CleanMedia
from apps.core.classes.file_processing import FileProcessing
from apps.core.classes.image_optimizer import ImageOptimizer


current_year = datetime.date.today().year

def image_upload_path(instance, filename):
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenerated()
    return 'company/history/{filename}'.format(filename=filename)

class History(models.Model):
    year  = models.PositiveIntegerField('Год', validators=[MinValueValidator(2005), MaxValueValidator( current_year + 1 )], default=current_year, unique=True)
    body  = RichTextField('Описание', blank=True, null=True)
    image = models.ImageField('Изображение', upload_to=image_upload_path, blank=True, null=True)

    # Thumbnails for admin
    def image_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image.url))
    image_thumb.short_description = 'Изображение (thumbnail)'
    # Thumbnails for admin

    def __str__(self):
        return str(self.year)

    class Meta:
        verbose_name = 'Блок (История компании)'
        verbose_name_plural = 'История компании (Блоки)'


@receiver(post_save, sender=History)
def image_optimization(sender, instance, created, **kwargs):
    if instance.image:
        image = ImageOptimizer(instance.image.path)
        image.optimizeAndSaveImg()


@receiver(post_delete, sender=History)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
