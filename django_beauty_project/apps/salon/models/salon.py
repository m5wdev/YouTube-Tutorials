from django.db import models


class Salon(models.Model):
    active      = models.BooleanField('Активный', default=True, help_text='Опубликован или нет')
    name        = models.CharField('Название', max_length=255, db_index=True)
    description = models.TextField('Описание', blank=True, null=True)

    phone       = models.CharField('Телефон', max_length=100, blank=True, null=True)
    email       = models.EmailField('Email', max_length=200, blank=True, null=True)
    site_url    = models.URLField('Site URL', max_length=200, blank=True, null=True)

    created     = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'