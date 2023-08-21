from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from apps.company.serializers.category import CategorySerializer
from apps.company.models.category import Category

class CategoryViewSet(viewsets.ViewSet):
    """
    Класс представлений для модели Brand
    """

    def list(self, request):
        """
        Возвращает список всех брендов
        """
        categories = categories = Category.objects.filter(parent_category__isnull=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Возвращает бренд по id
        """

        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def retrieve_name_for_slug(self, request, name=None):
        """
        Возвращает slug категории по имени
        """

        category = Category.objects.get(name = name)
        return Response({'slug':category.slug})

    def get_comany_by_slug(self, request, slug=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


@api_view(['GET'])
def get_category_search(request):
    search = request.GET.get('search')
    if search:
        queryset = Category.objects.filter(name__iregex=search).distinct().order_by('name')
    else:
        queryset = Category.objects.all().distinct().order_by('name')[:50]
    serializer = CategorySerializer(queryset, many=True)
    return Response(serializer.data)
    # if len(search) >= 2:
    #     # queryset = Category.objects.filter(name__iregex=search).distinct()[:10]
    #     queryset = Category.objects.filter(name__istartswith=search).distinct()
    #     serializer = CategorySerializer(queryset, many=True)
    #     return Response(serializer.data)
    # else:
    #     return Response(status=status.HTTP_411_LENGTH_REQUIRED)
