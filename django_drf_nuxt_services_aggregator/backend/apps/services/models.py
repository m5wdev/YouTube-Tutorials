from django.db import models
from apps.company.models.company import Company
from classes.utils.transliterate import generate_slug


class CategoryService(models.Model):
    name = models.CharField('Название Категории для услуги', unique=True, max_length=255)
    parent_category = models.ForeignKey('self', verbose_name='Родительская категория', related_name='children_category_service', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'services_categories'
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуг'


class Service(models.Model):
    name      = models.CharField('Название услуги', max_length=255)
    slug      = models.SlugField('Slug', max_length=255, blank=True, null=True)
    price     = models.PositiveIntegerField('Цена (от)', blank=True, null=True)
    price_max = models.PositiveIntegerField('Цена (до)', blank=True, null=True)
    category  = models.ForeignKey(CategoryService, related_name='service',
                                                    blank=True, null=True, on_delete=models.CASCADE,
                                                    verbose_name='Категория услуги')
    company   = models.ForeignKey(Company, related_name='services',
                                            blank=True, null=True, on_delete=models.CASCADE,
                                            verbose_name='Компания')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'services'
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
