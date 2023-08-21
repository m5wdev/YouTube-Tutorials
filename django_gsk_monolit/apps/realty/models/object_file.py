from django.db import models

from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.core.classes.clean_media import CleanMedia
from apps.core.classes.file_processing import FileProcessing

from apps.realty.models.object import Object


def file_upload_path(instance, filename):
    filename = FileProcessing(filename)
    filename = filename.newFileNameTranslitSlugify()
    return f'objects/{instance.object.crm_id}/files/{filename}'

class ObjectFile(models.Model):
    # FILE_TYPES = (
    #     ('info_booklet', 'Информационный буклет'),
    #     ('object_genplan', 'Генплан объекта недвижимости'),
    #     ('commercial_offer', 'Коммерческое предложение'),
    # )

    object    = models.ForeignKey(Object, on_delete=models.CASCADE, default=0)
    # name   = models.CharField('Название', max_length=100, choices=FILE_TYPES, blank=True, null=True)
    name      = models.CharField('Название', max_length=255)
    file      = models.FileField('Файл', upload_to=file_upload_path, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Файл Объекта'
        verbose_name_plural = 'Файлы Объектов'


@receiver(post_delete, sender=ObjectFile)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
