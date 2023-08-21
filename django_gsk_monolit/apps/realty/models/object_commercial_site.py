from django.db import models
from django.db.models import Q, Count, Min, Max

from django.urls import reverse
from django.utils.html import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from ckeditor.fields import RichTextField

from apps.realty.models.object_commercial import ObjectCommercial
from apps.realty.models.object_block import ObjectBlock
from apps.realty.models.object_section import ObjectSection

from apps.core.classes.clean_media import CleanMedia
from apps.core.classes.file_processing import FileProcessing
from apps.core.classes.image_optimizer import ImageOptimizer


class ObjectCommercialSiteQuerySet(models.QuerySet):
    def active(self):
        return Q(active=True)

    def get_all_active_sites_object(self, object_commercial_id):
        return self.active() & Q(object_commercial=object_commercial_id)

    def get_object_sites(self, object_commercial_id):
        return self.active() & self.get_all_active_sites_object(object_commercial_id)

    def object_sites_info_aggregated(self, object_commercial_id):
        sites = self.get_object_sites(object_commercial_id)
        return self.aggregate(
            object_total_sites_qty=Count('id', filter=sites),
            object_min_site_area=Min('site_area', filter=sites),
            object_max_site_area=Max('site_area', filter=sites),
            object_min_site_price=Min('price_total', filter=sites),
        )


def image_upload_path(instance, filename):
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenerated()
    return f'objects-commercial/{instance.object_commercial.crm_id}/sites/{instance.crm_id}/{filename}'

class ObjectCommercialSite(models.Model):
    SITE_TYPES = (
        ('office', 'Офис'),
        ('free-use', 'Помещение свободного назначения'),
    )

    # QuerySet
    objects = ObjectCommercialSiteQuerySet.as_manager()

    active            = models.BooleanField('Активный', default=True, help_text='Опубликован на сайте')
    special_offer     = models.BooleanField('Спецпредложение', default=False)

    object_commercial = models.ForeignKey(ObjectCommercial, verbose_name='Коммерческий Объект', on_delete=models.CASCADE)
    site_type         = models.CharField('Тип помещения', max_length=100, choices=SITE_TYPES)

    object_section    = models.ForeignKey(ObjectSection, verbose_name='Секция Объекта', on_delete=models.SET_NULL, blank=True, null=True)
    crm_id            = models.CharField('CRM ID', max_length=100, unique=True, help_text='ID объекта в 1C (Заполняется автоматически при выгрузке)')

    price_per_square  = models.DecimalField('Цена за м2 (руб.)', max_digits=8, decimal_places=2, blank=True, null=True, help_text='Стоимость одного квадратного метра')
    price_total       = models.DecimalField('Общая стоимость (руб.)', max_digits=11, decimal_places=2, blank=True, null=True, help_text='Считается автоматически из Площади помещения * Цена за м2')

    site_area         = models.DecimalField('Площадь помещения м2', max_digits=6, decimal_places=2, blank=True, null=True, help_text='Пример: 115.5 м2')
    floor             = models.IntegerField('Этаж', validators=[MinValueValidator(-5), MaxValueValidator(100)], blank=True, null=True)
    site_number       = models.CharField('Номер помещения', max_length=100, blank=True, null=True)
    ceiling_height    = models.DecimalField('Высота потолка (м)', max_digits=4, decimal_places=2, blank=True, null=True, help_text='Пример: 2.30 = 2 метра 30 см')
    street_entrance   = models.BooleanField('Вход с улицы', default=False)

    image_planning          = models.ImageField('Планировка', upload_to=image_upload_path, blank=True, null=True)
    image_floor             = models.ImageField('Квартира на этаже', upload_to=image_upload_path, blank=True, null=True, help_text='Планировка квартиры на этаже')
    image_section           = models.ImageField('Этаж в секции', upload_to=image_upload_path, blank=True, null=True, help_text='Выделенный этаж в секции объекта')
    image_section_in_object = models.ImageField('Секция в доме', upload_to=image_upload_path, blank=True, null=True, help_text='Выделенная секция в доме')
    image_genplan           = models.ImageField('Дом на генплане', upload_to=image_upload_path, blank=True, null=True, help_text='Выделенный дом на генплане')

    updated           = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)

    # Thumbnails for admin
    def image_planning_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image_planning.url))
    image_planning_thumb.short_description = 'Планировка (thumbnail)'
    # END Thumbnails for admin

    def __str__(self):
        return self.crm_id

    def get_absolute_url(self):
        return reverse('sites-commercial:detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Коммерческое помещение'
        verbose_name_plural = '2.1 Коммерческие Помещения (Офисы, Кладовые, Паркоместа)'

    def display_name_card(self):
        site_type_name = ''
        if self.site_type == 'free-use':
            site_type_name = 'Помещение'
        else:
            site_type_name = self.get_site_type_display()
        return f'{site_type_name}'

    def display_name_full(self):
        object_type = self.object_commercial.object_type
        if self.object_commercial.object_type.name_declension:
            object_type = self.object_commercial.object_type.name_declension
        if self.site_number:
            return f'{self.display_name_card()} №{self.site_number} на {self.floor} этаже в {object_type} {self.object_commercial.name}'
        return f'{self.display_name_card()} на {self.floor} этаже в {object_type} {self.object_commercial.name}'


@receiver(pre_save, sender=ObjectCommercialSite)
def calculate_total_price(sender, instance, **kwargs):
    if instance.site_area is not None and instance.price_per_square is not None:
        instance.price_total = instance.site_area * instance.price_per_square


@receiver(post_save, sender=ObjectCommercialSite)
def image_optimization(sender, instance, created, **kwargs):
    if instance.image_planning:
        image = ImageOptimizer(instance.image_planning.path)
        image.optimizeAndSaveImg()


@receiver(post_delete, sender=ObjectCommercialSite)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
