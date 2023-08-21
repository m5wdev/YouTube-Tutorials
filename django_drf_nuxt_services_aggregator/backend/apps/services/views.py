from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Prefetch
from rest_framework.pagination import PageNumberPagination

# from apps.company.models.company import Company
from .models import Service, CategoryService
from .serializers import CategoryServicesSerializer, ServiceSerializer


class CustomPaginator(PageNumberPagination):
    """
    Пагинация для вывода отфильтрованного
    списка
    """

    page_size = 50
    page_size_query_param = 'page_size'

@api_view(('GET',))
def get_all_services(request):
    """
    Возвращает все услуги
    """
    slug_city = request.GET.get('slug_city')
    queryset = Service.objects.filter(company__city__subdomain__name=slug_city)
    # queryset = Service.objects.filter()


    serializer = ServiceSerializer(queryset ,many=True)
    return Response(serializer.data)


class CategoryServiceModelViewSet(viewsets.ModelViewSet):
    """
    Класс для создания и обновления модели Company
    """

    queryset = CategoryService.objects.all()
    serializer_class = CategoryServicesSerializer


    def get_company_categories(self, request, slug):
        queryset = CategoryService.objects \
                                        .filter(service__company__slug=slug) \
                                        .prefetch_related(
                                            Prefetch(
                                                        'service',
                                                        queryset=Service.objects.filter(company__slug=slug)
                                                    )
                                            ).distinct()
        serializer = CategoryServicesSerializer(queryset ,many=True)
        return Response(serializer.data)


    def get_service_for_city(self, request, slug_city):
        paginator = CustomPaginator()
        # queryset = Service.objects.filter(company__city__subdomain__name=slug_city)
        queryset = Service.objects.filter()

        context = paginator.paginate_queryset(queryset, request)
        serializer = ServiceSerializer(context ,many=True)

        return paginator.get_paginated_response(
            serializer.data
        )


    def get_service_name(self, request, slug_service):
        queryset = Service.objects.filter(slug=slug_service).first()
        serializer = ServiceSerializer(queryset)
        return Response(serializer.data)
