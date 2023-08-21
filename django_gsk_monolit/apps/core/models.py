from django.db import models
from apps.core.classes.singleton_model import SingletonModel


class SiteSettings(SingletonModel):
    site_title       = models.CharField('Site title', max_length=100, blank=True, null=True, help_text='site meta &lt;title&gt;, max 100 chars')
    site_description = models.TextField('Site description', max_length=150, blank=True, null=True, help_text='site meta description, max 150')

    site_email       = models.EmailField('Site Email', max_length=255, blank=True, null=True, help_text='Основной email')
    site_phone       = models.CharField('Site Phone', max_length=50, blank=True, null=True, help_text='Основной телефон, e.g.: +79784447711')

    site_instagram   = models.URLField('Instagram', max_length=255, blank=True, null=True, help_text='e.g.: https://instagram.com/monolit.crimea/')
    site_facebook    = models.URLField('Facebook', max_length=255, blank=True, null=True, help_text='e.g.: https://facebook.com/monolit')
    site_vk          = models.URLField('VK (ВКонтакте)', max_length=255, blank=True, null=True, help_text='e.g.: https://vk.com/monolit.crimea')
    site_telegram    = models.URLField('Telegram', max_length=255, blank=True, null=True, help_text='e.g.: https://t.me/monolitstroit')

    def __str__(self):
        return 'Основные настройки сайта'

    class Meta:
        verbose_name = 'Основные настройки сайта'
        verbose_name_plural = 'Основные настройки сайта'
