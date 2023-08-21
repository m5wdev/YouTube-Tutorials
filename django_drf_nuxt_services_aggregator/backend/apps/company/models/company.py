import os, uuid

from django.db import models
from django.utils.html import mark_safe
from django.core.validators import MinValueValidator, MaxValueValidator

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from classes.utils.transliterate import generate_slug

from apps.users.models import CustomUser
from apps.cities.models.city import City

from .brand import Brand
from .category import Category
from .point import Point
from .often_repair import OftenRepair


def company_logo_upload(instance, filename):
    name, ext = os.path.splitext(filename.lower())
    # new_name = f'logo{ext}'
    new_name = f'{uuid.uuid4()}{ext}'
    # return f'companies/{instance.city.subdomain}/{instance.slug}/{new_name}'
    return f'companies/logos/{new_name}'

class Company(models.Model):
    active = models.BooleanField('Активная', default=True)
    name   = models.CharField('Название компании', max_length=255, db_index=True)
    # slug   = models.SlugField('Slug', unique=True, blank=True, max_length=255)
    slug   = models.SlugField('Slug', blank=True, null=True, max_length=255)
    body   = models.TextField('Описание', blank=True, null=True)

    email = models.EmailField('Email', max_length=255, blank=True, null=True)
    url   = models.URLField('Сайт', max_length=255, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=255, blank=True, null=True)

    logo = ProcessedImageField(verbose_name='Логотип компании',
                                upload_to=company_logo_upload,
                                # processors=[ResizeToFill(1100, 800)],
                                #  options={'quality': 80},
                                # JPEG
                                processors=[ResizeToFit(512, 512)],
                                format='JPEG',
                                options={'quality': 75},
                                blank=True, null=True)

    courier_departure = models.BooleanField('Выезд курьера', default=False)
    master_departure  = models.BooleanField('Выезд мастера', default=False)
    free_diagnostics  = models.BooleanField('Бесплатная диагностика', default=False)
    quick_repair      = models.BooleanField('Срочный ремонт', default=False)
    pay_after_repair  = models.BooleanField('Ремонт без предоплаты', default=False)
    own_warehouse     = models.BooleanField('Собственный склад запчастей', default=False)
    free_parking      = models.BooleanField('Бесплатная парковка', default=False)
    fix_price         = models.BooleanField('Фиксированная стоимость ремонта', default=False)
    cash_pay          = models.BooleanField('Оплата наличными', default=False)
    card_pay          = models.BooleanField('Оплата картой', default=False)
    owner_register    = models.BooleanField('Владелец зарегистрирован', default=False)

    min_price = models.PositiveIntegerField('Минимальная цена', blank=True, null=True)
    max_price = models.PositiveIntegerField('Максимальная цена', blank=True, null=True)

    number_of_employees = models.PositiveIntegerField('Количество работников', blank=True, null=True, validators=[MinValueValidator(1)])
    year_of_foundation  = models.CharField('Год основания', max_length=255, blank=True, null=True)

    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE, blank=True, null=True)

    brands       = models.ManyToManyField(Brand,db_index=True,related_name='companies', verbose_name='Бренды', blank=True)
    categories   = models.ManyToManyField(Category, related_name='companies', verbose_name='Категории', blank=True)
    points       = models.ManyToManyField(Point, related_name='company', verbose_name='Мастерские', blank=True)
    often_repair = models.ManyToManyField(OftenRepair, verbose_name='Часто ремонтируем', blank=True)

    ya_id         = models.CharField('YA_ID', max_length=255, blank=True, null=True)
    ya_categories = models.TextField('YA_Categories', blank=True, null=True)
    ya_services   = models.TextField('YA_Services', blank=True, null=True)

    is_promo = models.BooleanField('Промо', default=False)
    promo    = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)

    author  = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Автор')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Thumbnails
    def logo_thumb(self):
        return mark_safe(f' \
                            <a href="{self.logo.url}" target="_blank"> \
                                <img style="width: 128px; height: auto;" src="{self.logo.url}" alt=""> \
                            </a> \
                        ')
    logo_thumb.short_description = 'Превью логотипа'
    # END Thumbnails

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            # self.slug = generate_slug(self.name)
            self.slug = generate_slug(self.name) + '-' + str(uuid.uuid4())
        return super().save(*args, **kwargs)

    def get_city_name(self):
        return self.city

    def get_author_name(self):
        return self.author

    class Meta:
        db_table = 'companies'
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
