from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver

from ckeditor.fields import RichTextField

from apps.core.classes.clean_media import CleanMedia
from apps.core.classes.file_processing import FileProcessing
from apps.core.classes.image_optimizer import ImageOptimizer


class Tender(models.Model):
    CATEGORIES = (
        ('construction', 'Строительство'),
        ('materials', 'Материалы'),
        ('equipment', 'Оборудование'),
        ('projecting', 'Проектирование'),
        ('other', 'Другое'),
    )

    active       = models.BooleanField('Активный', default=True, help_text='Является ли данный Тендер активным?')
    title        = models.CharField('Название тендера', max_length=255)
    category     = models.CharField('Категория тендера', max_length=100, choices=CATEGORIES)
    duties       = RichTextField('Обязанности', blank=True, null=True)
    requirements = RichTextField('Требования', blank=True, null=True)
    contacts     = RichTextField('Контакты', blank=True, null=True)
    date_start   = models.DateTimeField('Срок проведения (начало)', default=timezone.now)
    date_end     = models.DateTimeField('Срок проведения (конец)', default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тендер'
        verbose_name_plural = 'Тендеры'


def file_upload_path(instance, filename):
    tender_id = instance.tender.id
    filename = FileProcessing(filename)
    filename = filename.newFileNameTranslitSlugify()
    return 'company/tenders/{tender_id}/{filename}'.format(tender_id=tender_id, filename=filename)

class TenderFile(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, default=0)
    name   = models.CharField('Название документа', max_length=255)
    file   = models.FileField('Файл', upload_to=file_upload_path, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тендер (Файл)'
        verbose_name_plural = 'Тендеры (Файлы)'


class TenderFaq(models.Model):
    active   = models.BooleanField('Активный', default=True, help_text='Является ли данный вопрос-ответ активным?')
    order    = models.PositiveIntegerField('Порядок', default=0, blank=True, null=True, help_text='Чем выше число, тем ниже вопрос в списке')
    question = models.CharField('Вопрос', max_length=255)
    answer   = RichTextField('Ответ', blank=True, null=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос-ответ по Тендерам'
        verbose_name_plural = 'Тендеры (Вопросы-ответы)'


@receiver(post_delete, sender=TenderFile)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
