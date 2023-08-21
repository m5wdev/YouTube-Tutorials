from django.views.generic import View, TemplateView
from django.shortcuts import redirect

from apps.realty.models.object import Object
from apps.realty.models.object_site import ObjectSite
from apps.mortgage.models import Offer
from apps.news.models.news import News


class HomepageView(TemplateView):
    template_name = 'homepage/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        objects = Object.objects

        context['object_list'] = objects.filter(active=True, all_sold=False).order_by('?')[:8]
        context['objects_for_slider'] = objects.filter(active=True, all_sold=False).order_by('updated')[:7]
        context['objects_qty'] = objects.filter(active=True, all_sold=False).count()
        # context['objects_sold'] = Object.objects.filter(active=True, all_sold=True).order_by('order')
        context['mortgage_offers'] = Offer.objects.order_by('?')[:5]
        context['news_list'] = News.objects.filter(active=True).order_by('-updated')[:5]

        object_sites = ObjectSite.objects

        context['count_object_sites_room_0_site_area_min']   = object_sites.count_object_sites_site_area_min(0)
        context['count_object_sites_room_0_site_area_max']   = object_sites.count_object_sites_site_area_max(0)
        context['count_object_sites_room_0_price_total_min'] = object_sites.count_object_sites_price_total_min(0)

        context['count_object_sites_room_1_site_area_min']   = object_sites.count_object_sites_site_area_min(1)
        context['count_object_sites_room_1_site_area_max']   = object_sites.count_object_sites_site_area_max(1)
        context['count_object_sites_room_1_price_total_min'] = object_sites.count_object_sites_price_total_min(1)

        context['count_object_sites_room_2_site_area_min']   = object_sites.count_object_sites_site_area_min(2)
        context['count_object_sites_room_2_site_area_max']   = object_sites.count_object_sites_site_area_max(2)
        context['count_object_sites_room_2_price_total_min'] = object_sites.count_object_sites_price_total_min(2)

        context['count_object_sites_room_3_site_area_min']   = object_sites.count_object_sites_site_area_min(3)
        context['count_object_sites_room_3_site_area_max']   = object_sites.count_object_sites_site_area_max(3)
        context['count_object_sites_room_3_price_total_min'] = object_sites.count_object_sites_price_total_min(3)

        context['count_object_sites_room_4_site_area_min']   = object_sites.count_object_sites_site_area_min(4, 'gte')
        context['count_object_sites_room_4_site_area_max']   = object_sites.count_object_sites_site_area_max(4, 'gte')
        context['count_object_sites_room_4_price_total_min'] = object_sites.count_object_sites_price_total_min(4, 'gte')

        # Facet filters sites
        context['facet_filter_sites__summary'] = object_sites.sites_summary_info_aggregated()
        context['facet_filter_sites__rooms']   = ObjectSite.ROOMS_QTY
        # END Facet filters sites

        return context
