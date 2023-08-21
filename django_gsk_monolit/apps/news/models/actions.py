from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import mark_safe

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from imagekit.models import ProcessedImageField
# from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from ckeditor.fields import RichTextField

from apps.core.classes.clean_media import CleanMedia
from apps.core.classes.file_processing import FileProcessing
from apps.core.classes.image_optimizer import ImageOptimizer


def actions_image_upload_path(instance, filename):
    date = instance.date_start
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenerated()
    return 'actions/{date}/{filename}'.format(date=date, filename=filename)

class Actions(models.Model):
    active         = models.BooleanField('Активная', default=True, help_text='Опубликована на сайте')
    title          = models.CharField('Заголовок акции', max_length=255)
    date_start     = models.DateField('Дата начала акции', default=timezone.now)
    date_end       = models.DateField('Дата окончания акции', blank=True, null=True)
    description    = RichTextField('Описание акции', blank=True, null=True)
    partners_title = models.CharField('Заголовок для партнеров', max_length=255, blank=True, null=True)

    image_card     = ProcessedImageField(upload_to=actions_image_upload_path,
                                           processors=[ResizeToFill(1440, 900)],
                                           format='JPEG',
                                           options={'quality': 70},
                                           verbose_name='Изображение для карточки', blank=True, null=True)
    image_detail   = models.ImageField(upload_to=actions_image_upload_path, verbose_name='Изображение для страницы', blank=True, null=True)

    # Thumbnails for admin
    def image_card_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image_card.url))
    image_card_thumb.short_description = 'Изображение для карточки (thumbnail)'

    def image_detail_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image_detail.url))
    image_detail_thumb.short_description = 'Изображение для страницы (thumbnail)'
    # END Thumbnails for admin

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:actions:detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'


def actions_partner_logo_upload_path(instance, filename):
    filename = FileProcessing(filename)
    if instance.name:
        filename = filename.newFileNameFromField(instance.name, 'logo', None)
        return 'actions-partners/{filename}'.format(filename=filename)
    else:
        # TODO: Show message
        pass

class ActionsPartner(models.Model):
    action   = models.ForeignKey(Actions, verbose_name='Акция', on_delete=models.CASCADE)
    name     = models.CharField('Название партнера', max_length=255)
    logo     = models.ImageField(upload_to=actions_partner_logo_upload_path, verbose_name='Логотип партнера акции', blank=True, null=True)
    site_url = models.URLField('Сайт партнера', blank=True, null=True, help_text='Url сайта партнера')

    # Thumbnails for admin
    def logo_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.logo.url))
    logo_thumb.short_description = 'Логотип партнера акции (thumbnail)'
    # END Thumbnails for admin

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Партнер акции'
        verbose_name_plural = 'Партнеры акций'


@receiver(post_save, sender=Actions)
def actions_image_optimization(sender, instance, created, **kwargs):
    # if instance.image_for_card:
    #     image = ImageOptimizer(instance.image_for_card.path)
    #     image.optimizeAndSaveImg()
    if instance.image_for_detail:
        image = ImageOptimizer(instance.image_for_detail.path)
        image.optimizeAndSaveImg()


@receiver(post_delete, sender=Actions)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()


@receiver(post_save, sender=ActionsPartner)
def actions_image_optimization(sender, instance, created, **kwargs):
    if instance.logo:
        image = ImageOptimizer(instance.logo.path)
        image.optimizeAndSaveImg()


@receiver(post_delete, sender=ActionsPartner)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
