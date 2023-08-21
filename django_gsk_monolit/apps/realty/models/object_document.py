import datetime
from django.db import models

from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.core.classes.clean_media import CleanMedia
from apps.core.classes.file_processing import FileProcessing

from apps.realty.models.object import Object


def file_upload_path(instance, filename):
    object_crm_id = instance.object.crm_id
    filename = FileProcessing(filename)
    filename = filename.newFileNameTranslitSlugify()
    # filename = filename.newFileNameFromField(instance.title)
    return 'objects/{object_crm_id}/documents/{filename}'.format(object_crm_id=object_crm_id, filename=filename)

class ObjectDocumentAuthor(models.Model):
    name = models.CharField('Автор', max_length=255, unique=True, help_text='Пример: Иванов В.А.')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор документа'
        verbose_name_plural = 'Авторы документов'


class ObjectDocument(models.Model):
    object  = models.ForeignKey(Object, on_delete=models.CASCADE)
    title   = models.CharField('Название документа', max_length=255)
    author  = models.ForeignKey(ObjectDocumentAuthor, verbose_name='Автор', on_delete=models.SET_NULL, blank=True, null=True)
    date    = models.DateField(verbose_name='Дата', default=datetime.date.today)
    file    = models.FileField('Файл', upload_to=file_upload_path, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


@receiver(post_delete, sender=ObjectDocument)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
