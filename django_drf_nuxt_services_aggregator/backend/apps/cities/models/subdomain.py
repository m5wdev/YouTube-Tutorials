from django.db import models


class Subdomain(models.Model):
    name = models.SlugField('Поддомен', max_length=255, unique=True, help_text='e.g.: moscow')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subdomains'
        verbose_name = 'Поддомен'
        verbose_name_plural = 'Поддомены'
