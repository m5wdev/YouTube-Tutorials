import os
from django.conf import settings

from django.db.models import Count, Min, Max

from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.core.classes.render_to_pdf import RenderToPDF

from apps.realty.models.object import Object
from apps.realty.models.object_site import ObjectSite
from apps.realty.models.object_info_tab import ObjectInfoTab
from apps.realty.models.object_file import ObjectFile
from apps.realty.models.object_gallery import ObjectGallery, ObjectGalleryImage
from apps.realty.models.object_document import ObjectDocument
from apps.realty.models.object_video import ObjectVideo
from apps.realty.models.object_site_bathroom import ObjectBathroom
from apps.realty.models.object_site_balcony import ObjectBalcony
from apps.realty.models.object_elevator import ObjectElevator
from apps.realty.models.object_cities import ObjectCities
from apps.realty.models.object_section import ObjectSection

from apps.realty.models.object_commercial import ObjectCommercial
from apps.realty.models.object_commercial_site import ObjectCommercialSite

from apps.realty.models.object_commercial_info_tab import ObjectCommercialInfoTab

from apps.news.models.news import News
from apps.mortgage.models import Offer


class ObjectListView(ListView):
    model = Object
    queryset = Object.objects.filter(active=True, all_sold=False).order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Жилые объекты'
        context['objects_qty'] = Object.objects.filter(active=True, all_sold=False).count()
        context['objects_sold'] = Object.objects.filter(active=True, all_sold=True).order_by('order')
        return context


class ObjectDetailView(DetailView):
    model = Object
    queryset = Object.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = Object._meta
        context['page_title'] = f'{self.get_object().display_name()}'
        # context['page_meta_description'] = 'my custom meta'
        context['object_info_tabs'] = ObjectInfoTab.objects.filter(object_id=self.get_object().pk)
        context['object_files'] = ObjectFile.objects.filter(object_id=self.get_object().pk)
        context['object_galleries'] = ObjectGallery.objects.filter(object=self.get_object().pk).order_by('-order')
        context['object_galleries_images'] = ObjectGalleryImage.objects.filter(gallery__object=self.get_object().pk, gallery=context['object_galleries'].first())
        context['object_news'] = News.objects.filter(object=self.get_object().pk).order_by('-updated')
        context['other_objects'] = Object.objects.filter(active=True, all_sold=False).exclude(id=self.get_object().pk).order_by('?')[:4]
        context['object_videos'] = ObjectVideo.objects.filter(object=self.get_object().pk)

        context['object_special_offers'] = ObjectSite.objects.filter(object=self.get_object().pk, active=True, special_offer=True).order_by('?')[:3]
        context['object_special_offers_qty'] = ObjectSite.objects.filter(object=self.get_object().pk, active=True, special_offer=True).count()

        # ObjectDocument Pagination
        context['object_documents'] = ObjectDocument.objects.filter(object=self.get_object().pk).order_by('-updated')
        paginator = Paginator(context['object_documents'], 9)
        page_docs = self.request.GET.get('page-docs')
        try:
            context['object_documents'] = paginator.page(page_docs)
        except PageNotAnInteger:
            context['object_documents'] = paginator.page(1)
        except EmptyPage:
            context['object_documents'] = paginator.page(paginator.num_pages)
        # END ObjectDocument Pagination

        context['mortgage_offers'] = Offer.objects.filter(object=self.get_object().pk).order_by('rate_from')
        return context


class ObjectSiteListView(ListView):
    model = ObjectSite
    queryset = ObjectSite.objects.filter(active=True).order_by('-updated')
    # queryset = ObjectSite.objects.filter(active=True).order_by('price_total')
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Выбор жилой недвижимости'

        # Facet filters sites
        context['facet_filter_sites__summary'] = ObjectSite.objects.sites_summary_info_aggregated()
        context['facet_filter_sites__rooms']   = ObjectSite.ROOMS_QTY
        context['facet_filter_sites__objects'] = Object.objects.filter(active=True, all_sold=False).values('id', 'name').order_by('name')
        context['facet_filter_sites__cities']  = ObjectCities.objects.all()
        context['facet_filter_sites__years_of_comletition'] = ObjectSection.objects.filter(object_commercial__isnull=True).values('comlete_year').distinct().order_by('comlete_year')

        context['facet_filter_sites__sections'] = ObjectSection.objects.filter(object_commercial__isnull=True)
        # if object in GET request get related sections of objects
        object = self.request.GET.get('object')
        if object and object != 'all':
            context['facet_filter_sites__sections'] = ObjectSection.objects.filter(object_commercial__isnull=True, object=object)
        # END Facet filters sites

        context['count_sites_in_queryset'] = self.get_queryset().count()

        return context

    # Filter request with GET request parameters
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(active=True, object__all_sold=False)

        # GET parameters
        rooms = self.request.GET.getlist('rooms')
        if rooms and '4' in rooms:
            # add more rooms if selected 4
            rooms.extend(['5', '6', '7'])

        area_min = self.request.GET.get('area_min')
        area_max = self.request.GET.get('area_max')

        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')

        object = self.request.GET.get('object')
        if object == 'all':
            object = ''

        section = self.request.GET.get('section')
        city = self.request.GET.get('city')
        year = self.request.GET.get('year')

        floor_min = self.request.GET.get('floor_min')
        floor_max = self.request.GET.get('floor_max')

        if rooms:
            qs = qs.filter(rooms_qty__in=rooms)
        if area_min:
            qs = qs.filter(site_area__gte=area_min)
        if area_max:
            qs = qs.filter(site_area__lte=area_max)
        if price_min:
            qs = qs.filter(price_total__gte=price_min)
        if price_max:
            qs = qs.filter(price_total__lte=price_max)
        if object:
            qs = qs.filter(object=object)
        if section:
            qs = qs.filter(object_section=section)
        if city:
            qs = qs.filter(object__city=city)
        if year:
            qs = qs.filter(object_section__comlete_year=year)
        if floor_min:
            qs = qs.filter(floor__gte=floor_min)
        if floor_max:
            qs = qs.filter(floor__lte=floor_max)

        return qs.distinct()


class ObjectSiteDetailView(DetailView):
    model = ObjectSite
    queryset = ObjectSite.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = ObjectSite._meta
        context['page_title'] = self.get_object().display_name_full()
        # TODO: make more complicated and detailed query selection
        other_sites_query = ObjectSite.objects.filter(active=True, object=self.get_object().object.pk, rooms_qty=self.get_object().rooms_qty).exclude(id=self.get_object().pk)
        context['simular_sites'] = other_sites_query.order_by('?')[:3]
        context['simular_sites_count'] = other_sites_query.count()
        context['bathrooms'] = ObjectBathroom.objects.filter(object_site=self.get_object().pk)
        context['balconies'] = ObjectBalcony.objects.filter(object_site=self.get_object().pk)
        if self.get_object().object_section is not None:
            context['elevators'] = ObjectElevator.objects.filter(object_section=self.get_object().object_section.pk)
        context['mortgage_offers'] = Offer.objects.filter(object=self.get_object().object.pk).order_by('rate_from')
        return context


class ObjectSiteDetailViewPDF(View):
    def get(self, request, pk):
        object = ObjectSite.objects.filter(active=True).get(id=pk)
        filename = '[monolit.site] ' + getattr(object, 'site_type') + ' ID ' + getattr(object, 'crm_id')

        # Full path to Cirilic font
        path_to_static_dir = os.path.join(settings.BASE_DIR, 'static')
        path_to_fonts_dir = os.path.join(path_to_static_dir, 'fonts')
        path_to_font = os.path.join(path_to_fonts_dir, 'roboto_regular.ttf')

        # Full path to Monolit logo
        path_to_images_dir = os.path.join(path_to_static_dir, 'images')
        path_to_monolit_logo = os.path.join(path_to_images_dir, 'monolit-logo-text.png')

        context = {
            'page_title': object.display_name_full(),
            'font_path': path_to_font,
            'monolit_logo': path_to_monolit_logo,
            'object': object,
            'request': request,
        }
        return RenderToPDF.render('pdf/object_site_detail_pdf.html', context, filename)


class ObjectCommercialListView(ListView):
    model = ObjectCommercial
    queryset = ObjectCommercial.objects.filter(active=True, all_sold=False).order_by('order')
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Коммерческие Объекты'
        context['objects_commercial_qty'] = ObjectCommercial.objects.filter(active=True, all_sold=False).count()
        context['objects_commercial_sold'] = ObjectCommercial.objects.filter(active=True, all_sold=True).order_by('order')
        return context


class ObjectCommercialDetailView(DetailView):
    model = ObjectCommercial
    queryset = ObjectCommercial.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = ObjectCommercial._meta
        context['page_title'] = f'{self.get_object().display_name()}'
        context['object_info_tabs'] = ObjectCommercialInfoTab.objects.filter(object_commercial=self.get_object().pk)
        context['commercial_sites'] = ObjectCommercialSite.objects.filter(object_commercial=self.get_object().id, active=True).order_by('?')[:12]
        return context


class ObjectCommercialSiteListView(ListView):
    model = ObjectCommercialSite
    queryset = ObjectCommercialSite.objects.filter(active=True).order_by('-updated')
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Выбор коммерческой недвижимости'
        return context


class ObjectCommercialSiteDetailView(DetailView):
    model = ObjectCommercialSite
    queryset = ObjectCommercialSite.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opts'] = ObjectCommercialSite._meta
        context['page_title'] = self.get_object().display_name_full()
        return context


class ObjectCommercialSiteDetailViewPDF(View):
    def get(self, request, pk):
        object = ObjectCommercialSite.objects.filter(active=True).get(id=pk)
        filename = '[monolit.site] ' + getattr(object, 'site_type') + ' ID ' + getattr(object, 'crm_id')

        # Full path to Cirilic font
        path_to_static_dir = os.path.join(settings.BASE_DIR, 'static')
        path_to_fonts_dir = os.path.join(path_to_static_dir, 'fonts')
        path_to_font = os.path.join(path_to_fonts_dir, 'roboto_regular.ttf')

        # Full path to Monolit logo
        path_to_images_dir = os.path.join(path_to_static_dir, 'images')
        path_to_monolit_logo = os.path.join(path_to_images_dir, 'monolit-logo-text.png')

        context = {
            'page_title': object.display_name_full(),
            'font_path': path_to_font,
            'monolit_logo': path_to_monolit_logo,
            'object': object,
            'request': request,
        }
        return RenderToPDF.render('pdf/object_commercial_site_detail_pdf.html', context, filename)
