from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from apps.company.serializers.brand import BrandSerializer
from apps.company.models.brand import Brand

letter_ru = ["А","Б","В",
            "Г","Д","Е","Ё","Ж","З",
            "И","Й","К","Л","М","Н",
            "О","П","Р","С","Т","У",
            "Ф","Х","Ц","Ч","Ш","Щ",
            "Ъ","Ы","Ь","Э","Ю","Я"
            ]

class BrandViewSet(viewsets.ViewSet):
    """
    Класс представлений для модели Brand
    """

    def list(self, request):
        """
        Возвращает список всех брендов
        """
        popular = request.GET.get('popular')
        subdomain = request.GET.get('subdomain')
        if popular:
            # brands = Brand.objects.filter(popular = True,companies__city__subdomain__name=subdomain).order_by('name')[:30]
            brands = Brand.objects.filter(popular = True).order_by('name')[:30]
        else:
             brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """
        Возвращает бренд по id
        """
        queryset = Brand.objects.all()
        brand = get_object_or_404(queryset, pk=pk)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)

    def get_brand_letter(self, request, letter=None):
        """
        Возвращает бренд по id
        """
        subdomain = request.GET.get('subdomain')

        if letter == 'a-ya':
            list_letter_ru = [
                "А","Б","В","Г","Д",
                "Е","Ё","Ж","З","И",
                "Й","К","Л","М","Н",
                "О","П","Р","С","Т",
                "У","Ф","Х","Ц","Ч",
                "Ш","Щ","Ъ","Ы","Ь",
                "Э","Ю","Я"
                ]
            query = Q()
            for letter in list_letter_ru:
                query = query | Q(name__startswith=letter)
            queryset = Brand.objects.filter(
                query
                ).filter(companies__city__subdomain__name=subdomain).distinct()
        else:
            queryset = Brand.objects.filter(
                name__startswith = letter,
                companies__city__subdomain__name=subdomain
                ).distinct()

        serializer = BrandSerializer(queryset,many=True)
        return Response(serializer.data)


    def get_brand_by_slug(self, request, slug=None):
        queryset = Brand.objects.all()
        brand = get_object_or_404(queryset, slug=slug)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)


@api_view(['GET'])
def get_brand_search(request):
    search = request.GET.get('search')
    # queryset = Brand.objects.filter(name__iregex=search).distinct()
    queryset = Brand.objects.filter(name__istartswith=search).distinct()
    # queryset = Brand.objects.filter(name__icontains=search).distinct()
    serializer = BrandSerializer(queryset, many=True)
    return Response(serializer.data)
