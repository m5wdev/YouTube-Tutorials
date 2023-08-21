import datetime

# from django.shortcuts import render
from django.http import JsonResponse

from apps.salon.models.salon import Salon
from apps.salon.models.work_schedule import WorkSchedule
from apps.salon.models.address import Address, City

from apps.actions.models import Actions
from apps.services.models import Services


def api_salons_list_view(request):
    salons = Salon.objects.filter(active=True).values('id', 'name', 'description')

    actions = Actions.objects.filter(active=True)
    actions_salons_ids_list = list(set(actions.values_list('salon__id', flat=True)))

    now = datetime.datetime.now()
    today_weekday = datetime.datetime.today().weekday()
    now_time = f'{now.hour}:{now.minute}:{now.second}'

    for salon in salons:
        # Actions
        for action in actions:
            if salon['id'] in actions_salons_ids_list:
                salon['has_actions'] = True
            else:
                salon['has_actions'] = False

        #  Addresses
        salon['addresses'] = []
        salons_addresses = list(Address.objects.filter(salon__id=salon['id']).values('city__name', 'metro__name', 'street', 'building', 'latitude', 'longitude'))

        for salon_address in salons_addresses:
            salon_address['address_full'] = f"{salon_address['city__name']}, {salon_address['street']}, {salon_address['building']}"

            # Working schedule for address
            salon_address['working_schedule'] = {}
            address_working_schedules = WorkSchedule.objects.filter(address__salon__id=salon['id'], week_day=today_weekday)

            for aws in address_working_schedules:
                if int(aws.week_day) == int(today_weekday):
                    # Compare current time and Salon working_hours_to
                    if int(str(now_time).replace(':','')) < int(str(aws.working_hours_to).replace(':','')):
                        salon_address['working_schedule']['open_now'] = True
                    else:
                        salon_address['working_schedule']['open_now'] = False

                    salon_address['working_schedule']['open_from'] = aws.working_hours_from
                    salon_address['working_schedule']['open_to'] = aws.working_hours_to

            salon['addresses'].append(salon_address)

    salons_list = list(salons)
    return JsonResponse(salons_list, safe=False)


def api_cities_list_view(request):
    cities_list = list(City.objects.all().values('id', 'name'))
    return JsonResponse(cities_list, safe=False)


def api_services_list_view(request):
    services_list = list(Services.objects.all().values('id', 'parent', 'parent__name', 'name'))

    services_list_sorted = []
    for service in services_list:
        if service['parent'] == None:
            services_list_sorted.append(
                {
                    'id': service['id'],
                    'name': service['name'],
                    'services': []
                }
            )

    for service_sorted in services_list_sorted:
        query_tree = list(Services.objects.get(pk=service_sorted['id']).get_descendants(include_self=False).values('id', 'parent', 'parent__name', 'name'))
        service_sorted['services'].extend(query_tree)
    return JsonResponse(services_list_sorted, safe=False)