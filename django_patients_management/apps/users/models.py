from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import date


class CustomUser(AbstractUser):
    GENDERS = (
        ('m', 'Мужчина'),
        ('f', 'Женщина'),
    )

    fio        = models.CharField('ФИО', max_length=255, default='')
    gender     = models.CharField('Пол', max_length=1, choices=GENDERS, default='')
    birth_date = models.DateField('Дата рождения', default='2000-09-12')


class DoctorWorkSchedule(models.Model):
    STATES = (
        ('w', 'Прием'),
        ('r', 'Перерыв'),
        ('v', 'Отпуск'),
    )

    state      = models.CharField('Статус', max_length=1, choices=STATES, default='')
    doctor     = models.ForeignKey(CustomUser, verbose_name='Врач', on_delete=models.SET_NULL, blank=True, null=True, related_name='doctor')
    patient    = models.ForeignKey(CustomUser, verbose_name='Пациент', on_delete=models.SET_NULL, blank=True, null=True, related_name='patient')
    date       = models.DateField('Дата', default=date.today)
    time_start = models.TimeField('Время от', blank=True, null=True)
    time_end   = models.TimeField('Время до', blank=True, null=True)
