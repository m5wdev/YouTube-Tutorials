from django.db import models

from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.realty.models.object import Object

from apps.core.classes.video_utils import VideoUtils


class ObjectVideo(models.Model):
    object    = models.ForeignKey(Object, on_delete=models.CASCADE, default=0)
    video     = models.CharField('ID видео в YouTube', max_length=100, blank=True, null=True, help_text='Укажите ссылки вида: https://www.youtube.com/watch?v=JbacFR_B-jw или https://youtu.be/JbacFR_B-jw Либо ID видео в YouTube, например: JbacFR_B-jw')

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'


@receiver(pre_save, sender=ObjectVideo)
def get_youtube_video_code(sender, instance, **kwargs):
    if instance.video:
        instance.video = VideoUtils.get_youtube_video_id(instance.video)
