import math

from django.db import models
from django.db.models import Q, Count, Min, Max

from django.urls import reverse
from django.utils.html import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from apps.realty.models.object import Object
from apps.realty.models.object_block import ObjectBlock
from apps.realty.models.object_section import ObjectSection

from apps.core.classes.clean_media import CleanMedia
from apps.core.classes.file_processing import FileProcessing
from apps.core.classes.image_optimizer import ImageOptimizer


class ObjectSiteWindowsView(models.Model):
    name = models.CharField('Вид из окон', max_length=255)

    def __str__(self):
        return self.name


class ObjectSiteQuerySet(models.QuerySet):
    def active(self):
        return Q(active=True)

    def get_all_active_sites_object(self, object_id):
        return self.active() & Q(object=object_id)

    def get_object_sites(self, object_id):
        return self.active() & self.get_all_active_sites_object(object_id) & Q(site_type__in=['site', 'apartments'])

    def object_sites_info_aggregated(self, object_id):
        sites = self.get_object_sites(object_id)
        return self.aggregate(
            object_total_sites_qty=Count('id', filter=sites),
            object_min_site_area=Min('site_area', filter=sites),
            object_max_site_area=Max('site_area', filter=sites),
            object_min_site_price=Min('price_total', filter=sites),
        )

    def object_sites_info_by_rooms_aggregated(self, object_id, rooms_qty: int):
        if rooms_qty < 4:
            sites = self.get_object_sites(object_id) & Q(rooms_qty=rooms_qty)
        if rooms_qty >= 4:
            sites = self.get_object_sites(object_id) & Q(rooms_qty__in=[4, 5])
        return self.aggregate(
            sites_qty=Count('id', filter=sites),
            min_price=Min('price_total', filter=sites),
            min_area=Min('site_area', filter=sites),
            max_area=Max('site_area', filter=sites),
        )

    # ObjectSites rooms info
    def count_object_sites_site_area_min(self, rooms_qty:int, rooms_qty_query_type=None):
        if rooms_qty_query_type == 'gte':
            return self.filter(active=True, rooms_qty__gte=rooms_qty, site_type__in=['site', 'apartments']).aggregate(Min('site_area'))
        if rooms_qty_query_type == None:
            return self.filter(active=True, rooms_qty=rooms_qty, site_type__in=['site', 'apartments']).aggregate(Min('site_area'))

    def count_object_sites_site_area_max(self, rooms_qty:int, rooms_qty_query_type=None):
        if rooms_qty_query_type == 'gte':
            return self.filter(active=True, rooms_qty__gte=rooms_qty, site_type__in=['site', 'apartments']).aggregate(Max('site_area'))
        if rooms_qty_query_type == None:
            return self.filter(active=True, rooms_qty=rooms_qty, site_type__in=['site', 'apartments']).aggregate(Max('site_area'))

    def count_object_sites_price_total_min(self, rooms_qty:int, rooms_qty_query_type=None):
        if rooms_qty_query_type == 'gte':
            return self.filter(active=True, rooms_qty__gte=rooms_qty, site_type__in=['site', 'apartments']).aggregate(Min('price_total'))
        if rooms_qty_query_type == None:
            return self.filter(active=True, rooms_qty=rooms_qty, site_type__in=['site', 'apartments']).aggregate(Min('price_total'))
    # END ObjectSites rooms info

    def get_all_sites_in_all_objects(self):
        return self.active() & Q(object__all_sold=False) & Q(site_type__in=['site', 'apartments'])

    def sites_summary_info_aggregated(self):
        sites_total_qty = self.aggregate(sites_total_qty=Count('id', filter=self.get_all_sites_in_all_objects()))['sites_total_qty']

        # Round aggregated sites area and prices to avoid decimals in "facet filters sites" form inputs

        # round down
        min_sites_area = int( self.aggregate(min_sites_area=Min('site_area', filter=self.get_all_sites_in_all_objects()))['min_sites_area'] )

        # round up
        max_sites_area = math.ceil( self.aggregate(max_sites_area=Max('site_area', filter=self.get_all_sites_in_all_objects()))['max_sites_area'] )
        # min_sites_area = round( self.aggregate(min_sites_area=Min('site_area', filter=self.get_all_sites_in_all_objects()))['min_sites_area'], 1 )
        # max_sites_area = round( self.aggregate(max_sites_area=Max('site_area', filter=self.get_all_sites_in_all_objects()))['max_sites_area'], 1 )

        # round down
        min_price = int( self.aggregate(min_price=Min('price_total', filter=self.get_all_sites_in_all_objects()))['min_price'] )

        # round up
        max_price = math.ceil( self.aggregate(max_price=Max('price_total', filter=self.get_all_sites_in_all_objects()))['max_price'] )
        # min_price = round( self.aggregate(min_price=Min('price_total', filter=self.get_all_sites_in_all_objects()))['min_price'] )
        # max_price = round( self.aggregate(max_price=Max('price_total', filter=self.get_all_sites_in_all_objects()))['max_price'] )

        min_floor = self.aggregate(min_floor=Min('floor', filter=self.get_all_sites_in_all_objects()))['min_floor']
        max_floor = self.aggregate(max_floor=Max('floor', filter=self.get_all_sites_in_all_objects()))['max_floor']

        return {
            'sites_total_qty': sites_total_qty,

            'min_sites_area': min_sites_area,
            'max_sites_area': max_sites_area,

            'min_price': min_price,
            'max_price': max_price,

            'min_floor': min_floor,
            'max_floor': max_floor,
        }


def image_upload_path(instance, filename):
    filename = FileProcessing(filename)
    filename = filename.newFileNameGenerated()
    return f'objects/{instance.object.crm_id}/sites/{instance.crm_id}/{filename}'

class ObjectSite(models.Model):
    SITE_TYPES = (
        ('site', 'Квартира'),
        ('apartments', 'Апартаменты'),
    )

    ROOMS_QTY = (
        ('0', 'Студия'),
        ('1', '1 комнатная'),
        ('2', '2 комнатная'),
        ('3', '3 комнатная'),
        ('4', '4 комнатная'),
        ('5', '5 комнатная'),
    )

    FINISHING_TYPES = (
        ('0', 'Без отделки'),
        ('1', 'Черновая'),
        ('2', 'Чистовая'),
    )

    # QuerySet
    objects = ObjectSiteQuerySet.as_manager()

    active                  = models.BooleanField('Активный', default=True, help_text='Опубликован на сайте')
    special_offer           = models.BooleanField('Спецпредложение', default=False)

    object                  = models.ForeignKey(Object, verbose_name='Жилой Объект', on_delete=models.CASCADE)
    site_type               = models.CharField('Тип помещения', max_length=100, choices=SITE_TYPES)

    object_section          = models.ForeignKey(ObjectSection, verbose_name='Секция Объекта', on_delete=models.SET_NULL, blank=True, null=True)

    crm_id                  = models.CharField('CRM ID', max_length=100, unique=True, help_text='ID объекта в 1C (Заполняется автоматически при выгрузке)')

    price_per_square        = models.DecimalField('Цена за м2 (руб)', max_digits=8, decimal_places=2, blank=True, null=True, help_text='Стоимость одного квадратного метра')
    price_total             = models.DecimalField('Общая стоимость (руб)', max_digits=11, decimal_places=2, blank=True, null=True, help_text='Считается автоматически из Площади помещения * Цена за м2')

    site_area               = models.DecimalField('Площадь помещения м2', max_digits=6, decimal_places=2, blank=True, null=True, help_text='Пример: 65.5 м2')
    living_area             = models.DecimalField('Жилая площадь м2', max_digits=6, decimal_places=2, blank=True, null=True, help_text='Пример: 42 м2')
    kitchen_area            = models.DecimalField('Площадь кухни м2', max_digits=5, decimal_places=2, blank=True, null=True, help_text='Пример: 12.7 м2')

    floor                   = models.IntegerField('Этаж', validators=[MinValueValidator(-5), MaxValueValidator(100)], blank=True, null=True)
    site_number             = models.CharField('Номер квартиры', max_length=100, blank=True, null=True)
    rooms_qty               = models.CharField('Количество комнат', max_length=100, choices=ROOMS_QTY, blank=True, null=True)
    ceiling_height          = models.DecimalField('Высота потолка (м)', max_digits=4, decimal_places=2, blank=True, null=True, help_text='Пример: 2.30 = 2 метра 30 см')
    two_levels              = models.BooleanField('Двухуровневая квартира', default=False, help_text='Квартира с полноценным 2-м этажом')
    entresol                = models.BooleanField('Антресоль', default=False, help_text='Наличие в квартире этажа-антресоли')
    wardrobe                = models.BooleanField('Гардеробная', default=False, help_text='Помещение для гардеробной или кладовой')
    finish_type             = models.CharField('Отделка', max_length=100, choices=FINISHING_TYPES, blank=True, null=True)
    window_view             = models.ManyToManyField(ObjectSiteWindowsView, verbose_name='Вид из окон', blank=True)

    image_planning          = models.ImageField('Планировка', upload_to=image_upload_path, blank=True, null=True)
    image_planning3d        = models.ImageField('Планировка 3D', upload_to=image_upload_path, blank=True, null=True)
    image_floor             = models.ImageField('Квартира на этаже', upload_to=image_upload_path, blank=True, null=True, help_text='Планировка квартиры на этаже')
    image_section           = models.ImageField('Этаж в секции', upload_to=image_upload_path, blank=True, null=True, help_text='Выделенный этаж в секции объекта')
    image_section_in_object = models.ImageField('Секция в доме', upload_to=image_upload_path, blank=True, null=True, help_text='Выделенная секция в доме')
    image_genplan           = models.ImageField('Дом на генплане', upload_to=image_upload_path, blank=True, null=True, help_text='Выделенный дом на генплане')

    updated                 = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)

    # Thumbnails for admin
    def image_planning_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image_planning.url))
    image_planning_thumb.short_description = 'Планировка (thumbnail)'

    def image_planning3d_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image_planning3d.url))
    image_planning3d_thumb.short_description = 'Планировка 3D (thumbnail)'

    def image_floor_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image_floor.url))
    image_floor_thumb.short_description = 'Квартира на этаже (thumbnail)'

    def image_section_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image_section.url))
    image_section_thumb.short_description = 'Этаж в секции (thumbnail)'

    def image_section_in_object_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image_section_in_object.url))
    image_section_in_object_thumb.short_description = 'Секция в доме (thumbnail)'

    def image_genplan_thumb(self):
        return mark_safe('<img src="{}" alt="" style="width: 256px; height: auto;" />'.format(self.image_genplan.url))
    image_genplan_thumb.short_description = 'Дом на генплане (thumbnail)'
    # END Thumbnails for admin

    def __str__(self):
        return self.crm_id

    def get_absolute_url(self):
        return reverse('sites:detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Жилое помещение'
        verbose_name_plural = '1.1 Жилые Помещения (Квартиры, Апартаменты)'

    def display_name_card(self):
        site_type_name = ''
        # Квартира
        if self.site_type == 'site':
            site_type = 'квартира'

            if self.rooms_qty == '0':
                site_type_name = f'{site_type.title()}-cтудия'
            elif self.rooms_qty == '1':
                site_type_name = f'1 комнатная {site_type}'
            elif self.rooms_qty == '2':
                site_type_name = f'2 комнатная {site_type}'
            elif self.rooms_qty == '3':
                site_type_name = f'3 комнатная {site_type}'
            elif self.rooms_qty == '4':
                site_type_name = f'4 комнатная {site_type}'
            elif self.rooms_qty == '5':
                site_type_name = f'5-комнатная {site_type}'
        # Апартаменты
        elif self.site_type == 'apartments':
            site_type = 'апартаменты'

            if self.rooms_qty == '0':
                site_type_name = f'{site_type.title()}-cтудия'
            elif self.rooms_qty == '1':
                site_type_name = f'1 комнатные {site_type}'
            elif self.rooms_qty == '2':
                site_type_name = f'2 комнатные {site_type}'
            elif self.rooms_qty == '3':
                site_type_name = f'3 комнатные {site_type}'
            elif self.rooms_qty == '4':
                site_type_name = f'4 комнатные {site_type}'
            elif self.rooms_qty == '5':
                site_type_name = f'5 комнатные {site_type}'
        return f'{site_type_name}'

    def display_name_full(self):
        site_type_name = ''
        # Квартира
        if self.site_type == 'site':
            site_type = 'квартира'

            if self.rooms_qty == '0':
                site_type_name = f'{site_type.title()}-cтудия'
            elif self.rooms_qty == '1':
                site_type_name = f'1 комнатная {site_type}'
            elif self.rooms_qty == '2':
                site_type_name = f'2 комнатная {site_type}'
            elif self.rooms_qty == '3':
                site_type_name = f'3 комнатная {site_type}'
            elif self.rooms_qty == '4':
                site_type_name = f'4 комнатная {site_type}'
            elif self.rooms_qty == '5':
                site_type_name = f'5 комнатная {site_type}'

        # Апартаменты
        elif self.site_type == 'apartments':
            site_type = 'апартаменты'

            if self.rooms_qty == '0':
                site_type_name = f'{site_type.title()}-cтудия'
            elif self.rooms_qty == '1':
                site_type_name = f'1 комнатные {site_type}'
            elif self.rooms_qty == '2':
                site_type_name = f'2 комнатные {site_type}'
            elif self.rooms_qty == '3':
                site_type_name = f'3 комнатные {site_type}'
            elif self.rooms_qty == '4':
                site_type_name = f'4 комнатные {site_type}'
            elif self.rooms_qty == '5':
                site_type_name = f'5 комнатные {site_type}'

        object_type_name = self.object.object_type.name_declension
        if self.object.object_type.name == 'Жилой комплекс' and self.object.object_type.name_abbreviation:
            object_type_name = self.object.object_type.name_abbreviation

        if self.site_number:
            return f'{site_type_name} №{self.site_number} на {self.floor} этаже в {object_type_name} {self.object.name}'
        return f'{site_type_name} на {self.floor} этаже в {object_type_name} {self.object.name}'


@receiver(pre_save, sender=ObjectSite)
def calculate_total_price(sender, instance, **kwargs):
    if instance.site_area is not None and instance.price_per_square is not None:
        instance.price_total = instance.site_area * instance.price_per_square


@receiver(post_save, sender=ObjectSite)
def image_optimization(sender, instance, created, **kwargs):
    if instance.image_planning:
        image = ImageOptimizer(instance.image_planning.path)
        image.optimizeAndSaveImg()
    if instance.image_planning3d:
        image = ImageOptimizer(instance.image_planning3d.path)
        image.optimizeAndSaveImg()
    if instance.image_floor:
        image = ImageOptimizer(instance.image_floor.path)
        image.optimizeAndSaveImg()
    if instance.image_section:
        image = ImageOptimizer(instance.image_section.path)
        image.optimizeAndSaveImg()
    if instance.image_section_in_object:
        image = ImageOptimizer(instance.image_section_in_object.path)
        image.optimizeAndSaveImg()
    if instance.image_genplan:
        image = ImageOptimizer(instance.image_genplan.path)
        image.optimizeAndSaveImg()


@receiver(post_delete, sender=ObjectSite)
def clean_empty_media_dirs(sender, instance, **kwargs):
    cleanMedia = CleanMedia()
    # Delete empty dirs in /media/
    cleanMedia.deleteEmptyDirsRecusive()
