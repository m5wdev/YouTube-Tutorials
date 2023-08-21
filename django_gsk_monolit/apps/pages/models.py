from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Pages(models.Model):
    active = models.BooleanField('Активная', default=True, help_text='Опубликована на сайте')
    title  = models.CharField('Заголовок страницы', max_length=255)
    slug   = models.SlugField('URL адрес', max_length=100, unique=True, help_text='e.g.: about-us (max 100 chars), получим https://monolit.site/about-us/')
    body   = RichTextField('Текст', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
