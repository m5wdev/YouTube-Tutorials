from django.db import models


class Blog(models.Model):
    GROUP_CHOICES = (
        ('1', 'Политика конфиденциальности'),
        ('2', 'Условия и положения'),
        ('3', 'Новости'),
    )

    title       = models.CharField('Заголовок', max_length=255)
    description = models.TextField('Описание', blank=True, null=True)
    meta_title  = models.CharField('Мета Заголовка', max_length=255, blank=True, null=True)
    meta_descr  = models.TextField('Мета Описания', blank=True, null=True)
    group_name  = models.CharField('Группа записи', max_length=255, choices=GROUP_CHOICES, default='1', blank=True, null=True)

    class Meta:
        db_table = 'blog'
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
