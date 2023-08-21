from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import mark_safe

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from ckeditor.fields import RichTextField

from apps.core.classes.clean_media import CleanMedia
from apps.core.classes.file_processing import FileProcessing
from apps.core.classes.image_optimizer import ImageOptimizer

from apps.realty.models.object import Object


class NewsCategory(models.Model):
    name = models.CharField('Имя категории', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Новостная категория'
        verbose_name_plural = 'Категории новостей'


def main_image_upload_path(instance, filename):
    date = instance.date
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenerated()
    return 'news/{date}/{filename}'.format(date=date, filename=filename)

class News(models.Model):
    active           = models.BooleanField('Активная', default=True, help_text='Опубликована на сайте')
    title            = models.CharField('Заголовок новости', max_length=255)
    object           = models.ManyToManyField(Object, verbose_name='Объект(ы)', blank=True, help_text='Относится ли данная новость к Объекту(ам) недвижимости? Если нет, то оставьте пустым')
    category         = models.ManyToManyField(NewsCategory, blank=True, verbose_name='Категории новости')
    date             = models.DateField(verbose_name='Дата', default=timezone.now)

    main_image       = models.ImageField(upload_to=main_image_upload_path, verbose_name='Главное изображение', blank=True, null=True)
    main_image_thumb = ImageSpecField(source='main_image', processors=[ResizeToFit(512, 512)], format='JPEG', options={'quality': 70})

    body             = RichTextField('Текст новости', blank=True, null=True)
    # created          = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated          = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Thumbnails for admin
    def main_image_admin_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 386px; height: auto;" />'.format(self.main_image.url))
    main_image_admin_thumb.short_description = 'Главное изображение (thumbnail)'
    # END Thumbnails for admin

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


def image_upload_path(instance, filename):
    date = instance.news.date
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenerated()
    return 'news/{date}/{filename}'.format(date=date, filename=filename)

class NewsImage(models.Model):
    news  = models.ForeignKey(News, verbose_name='Новость', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_path, verbose_name='Изображение', blank=True, null=True)

    # Thumbnails for admin
    def image_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image.url))
    image_thumb.short_description = 'Изображение (thumbnail)'
    # END Thumbnails for admin

    def __str__(self):
        return '{1} (image {0})'.format(self.id, self.news)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


@receiver(post_save, sender=News)
def main_image_optimization(sender, instance, created, **kwargs):
    if instance.main_image:
        image = ImageOptimizer(instance.main_image.path)
        image.optimizeAndSaveImg()

@receiver(post_delete, sender=News)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete imagekit chache file
    cleanMedia.cleanImagekitCacheImage(instance.main_image_thumb)
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()


@receiver(post_save, sender=NewsImage)
def image_optimization(sender, instance, created, **kwargs):
    if instance.image:
        image = ImageOptimizer(instance.image.path)
        image.optimizeAndSaveImg()


@receiver(post_delete, sender=NewsImage)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
