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
    return 'company/job/{filename}'.format(filename=filename)

class JobBlock(models.Model):
    title = models.CharField('Заголовок', max_length=255, blank=True, null=True)
    body  = RichTextField('Описание', blank=True, null=True)
    image = models.ImageField('Изображение', upload_to=image_upload_path, blank=True, null=True)
    order = models.PositiveIntegerField('Порядок', default=0, help_text='Чем выше число, тем ниже объект в списке')

    # Thumbnails for admin
    def image_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image.url))
    image_thumb.short_description = 'Изображение (thumbnail)'
    # Thumbnails for admin

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'Блок (Работа в компании)'
        verbose_name_plural = 'Работа в компании (Блоки)'


class JobVacancy(models.Model):
    title        = models.CharField('Название должности', max_length=255)
    experience   = models.CharField('Опыт', max_length=255, blank=True, null=True, help_text='Требования к опыту соискателя')
    duties       = RichTextField('Обязанности', blank=True, null=True, help_text='Описание должностных обязанностей')
    requirements = RichTextField('Требования к соискателю', blank=True, null=True)
    terms        = RichTextField('Условия', blank=True, null=True, help_text='Условия работы или преимущества компании')
    salary       = models.CharField('Зарплата', max_length=255, blank=True, null=True, help_text='Например: от 50 000 руб. или по результатам собеседования')
    contacts     = RichTextField('Контакты', blank=True, null=True, help_text='Контактные данные лица связанного с данной вакансией')
    order        = models.PositiveIntegerField('Порядок', default=0, help_text='Чем выше число, тем ниже объект в списке')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия (Работа в компании)'
        verbose_name_plural = 'Работа в компании (Вакансии)'


@receiver(post_save, sender=JobBlock)
def image_optimization(sender, instance, created, **kwargs):
    if instance.image:
        image = ImageOptimizer(instance.image.path)
        image.optimizeAndSaveImg()


@receiver(post_delete, sender=JobBlock)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
