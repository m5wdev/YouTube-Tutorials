from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from apps.salon.models.salon import Salon
from apps.salon.models.salon_services import SalonServices
from apps.salon.models.address import Address, City, Metro

from apps.actions.models import Actions
from apps.services.models import Services


class HomepageView(TemplateView):
    template_name = 'homepage/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Homepage'
        context['actions'] = Actions.objects.filter(active=True).order_by('?')[:4]
        return context


def search_results_view(request):
    context = {}
    context['page_title'] = 'Результаты поиска'
    context['filter_metro'] = Metro.objects.all()


    if request.GET.get('city'):
        get_city = request.GET.get('city')

        city_instance = City.objects.get(id=get_city)
        context['object_list'] = SalonServices.objects.filter(salon__active=True, address__city=city_instance)
    else:
        context['object_list'] = SalonServices.objects.filter(salon__active=True)


    if request.GET.get('service_to_add'):
        get_services = request.GET.get('service_to_add')

        get_services = get_services.split(",")
        get_services = map(int, get_services)
        get_services_list = list(set(get_services))
        context['object_list'] = SalonServices.objects.filter(salon__active=True, service__in=get_services_list)


    if request.GET.get('metro'):
        metro_stations_ids_list = list(map(int, request.GET.getlist('metro')))
        print(metro_stations_ids_list)
        context['object_list'] = context['object_list'].filter(address__metro__id__in=metro_stations_ids_list)

    return render(request, 'core/search-results.html', context)