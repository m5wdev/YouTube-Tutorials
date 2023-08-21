from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework import status
from rest_framework import viewsets

from .models.city import City
from .models.metro_line import MetroLine
from .models.metro_station import MetroStation

from .serializers.city import CitySerializer
from .serializers.metro_line import MetroLineSerializer
from .serializers.metro_station import MetroStationSerializer


@api_view(['GET'])
def get_city_name(request):
    """
    Возвращает имя города
    """
    # print(request.GET.get('slug_city'))
    slug = request.GET.get('slug_city')
    # if slug == 'localhost' or slug == 'servis-centers.ru':
    #     slug = 'moscow'
    print('ssssss',slug)
    try:
        cities = City.objects.get(subdomain__name = slug)
    except:
        cities = City.objects.get(subdomain__name = 'moscow')
    serilizer = CitySerializer(cities)
    return Response(serilizer.data)


@api_view(['GET'])
def get_cities_search(request):
    search = request.GET.get('search')
    queryset = City.objects.filter(name__iregex=search).distinct()[:10]
    serializer = CitySerializer(queryset,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_metro_city_search(request):
    city = request.GET.get('city')
    search = request.GET.get('search')
    queryset = MetroStation.objects.filter(city__id=city).filter(name__iregex=search).distinct()[:10]
    serializer = MetroStationSerializer(queryset,many=True)
    return Response(serializer.data)


class CityViewSet(viewsets.ViewSet):
    """
    Класс представлений для модели City
    """
    def list(self, request):
        """
        Возвращает список всех городов
        """
        cities = City.objects.all().order_by('name')
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Возвращает город по id
        """
        queryset = City.objects.all()
        city = get_object_or_404(queryset, pk=pk)
        serializer = CitySerializer(city)
        return Response(serializer.data)

    def get_metro_in_city(self, request, id=None):
        """
        Возвращает город по id
        """
        queryset = City.objects.get(id = id)
        if len(queryset.station_metro.all()) > 0:
            metro = True
        else:
            metro = False
        return Response({'metro':metro})


class MetroLineViewSet(viewsets.ViewSet):
    """
    Класс представлений для модели MetroLine
    """
    def list(self, request):
        """
        Возвращает список всех записей линий метро.
        Если присутствует параметр {city} возвращается
        отфильтрованный список линий метро по городам
        """
        city = request.GET.get('city')

        if city:
            metro_lines = MetroLine.objects.filter(station_metro__city_id=city)
        else:
            metro_lines = MetroLine.objects.all()
        serializer = MetroLineSerializer(metro_lines, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Возвращает линию метро по  id
        """
        queryset = MetroLine.objects.all()
        metro_line = get_object_or_404(queryset, pk=pk)
        serializer = MetroLineSerializer(metro_line)
        return Response(serializer.data)


class MetroStationViewSet(viewsets.ViewSet):
    """
    Класс представлений для модели MetroStation
    """
    def list(self, request):
        """
        Возвращает список всех записей линий метро.
        Если присутствует параметр {city} возвращается
        отфильтрованный список станций метро по городам .
        Если присутствует параметр {metro_line} возвращается
        отфильтрованный список станций метро по линиям метро.
        """
        metro_line = request.GET.get('metro_line')
        city = request.GET.get('city')

        if city:
            metro_stations = MetroStation.objects.filter(city__id=city)
        elif metro_line:
            metro_stations = MetroStation.objects.filter(
                metro_line__name=metro_line)
        else:
            metro_stations = MetroStation.objects.all()
        serializer = MetroStationSerializer(metro_stations, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Возвращает станцию метро по  id
        """
        queryset = MetroStation.objects.all()
        metro_station = get_object_or_404(queryset, pk=pk)
        serializer = MetroStationSerializer(metro_station)
        return Response(serializer.data)


def search_metro_line_city(self, request):
    """
    """
    metro_line = request.GET.get('metro_line')
    city = request.GET.get('city')

    if city:
        metro_stations = MetroStation.objects.filter(city__id=city)
    elif metro_line:
        metro_stations = MetroStation.objects.filter(metro_line__name=metro_line)
    else:
        metro_stations = MetroStation.objects.all()
    serializer = MetroStationSerializer(metro_stations, many=True)
    return Response(serializer.data)


def search_metro_station(self, request):
    """
    """
    metro_stantion = request.GET.get('metro_stantion')
    city = request.GET.get('city')

    if city:
        metro_stations = MetroStation.objects.filter(city__id=city)
    elif metro_stantion:
        metro_stations = MetroLine.objects.filter(metro_line__name=metro_stantion)
    else:
        metro_stations = MetroLine.objects.all()
    serializer = MetroStationSerializer(metro_stations, many=True)
    return Response(serializer.data)
