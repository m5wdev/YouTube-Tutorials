from django.db import models

from apps.salon.models.salon import Salon


class Client(models.Model):
    active     = models.BooleanField('Активный', default=True, help_text='Опубликован на сайте?')
    salon      = models.ForeignKey(Salon, verbose_name='Салон', on_delete=models.SET_NULL, null=True)
    phone      = models.CharField('Телефон', max_length=255)
    first_name = models.CharField('Имя', max_length=255)

    created    = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Клиент салона'
        verbose_name_plural = 'Клиенты салона'