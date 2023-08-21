from django.db import models
from classes.utils.transliterate import generate_slug


class OftenRepair(models.Model):
    name = models.CharField('Название услуги', unique=True, max_length=255)
    slug = models.SlugField('Slug', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'company_often_repair'
        verbose_name = 'Часто ремонтируем'
        verbose_name_plural = 'Часто ремонтируемые'
