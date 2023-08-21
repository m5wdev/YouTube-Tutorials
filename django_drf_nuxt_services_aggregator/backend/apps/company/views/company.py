# from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from apps.company.models.point import Point

from apps.company.serializers.company import (
    CompanySerializer,
    CompanySearchSerializer,
    CompanyUserSerializer
)
from apps.company.serializers.category import CategorySerializer
from apps.company.models.company import Company
from apps.company.models.category import Category
from apps.company.serializers.category import CategorySerializer
from apps.company.models.brand import Brand


class CustomPaginator(PageNumberPagination):
    """
    Пагинация для вывода отфильтрованного
    списка посылок
    """
    page_size = 25
    page_size_query_param = 'page_size'


class CompanyModelViewSet(viewsets.ModelViewSet):
    """
    Класс для создания и обновления модели Company
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_company_for_profile(self, request, pk):
        queryset = Company.objects.get(id=pk)
        serializer = CompanyUserSerializer(queryset)
        return Response(serializer.data)

    def get_slug(self, request, slug):
        queryset = Company.objects.get(slug=slug)
        serializer = CompanySerializer(queryset)
        return Response({'company': serializer.data})


@api_view(['GET'])
def get_count_home(request):
    subdomain = request.GET.get('subdomain')
    category_count = Category.objects.filter(
        companies__city__subdomain__name=subdomain).distinct().count()
    point_count = Point.objects.filter(
        city__subdomain__name=subdomain).distinct().count()
    company_count = Company.objects.filter(
        city__subdomain__name=subdomain).distinct().count()
    return Response({
        "category_count": category_count,
        "point_count": point_count,
        "company_count": company_count
    })


@api_view(['GET'])
def get_list_company(request, *args, **kwargs):
    """
    Выводит список всех компаний или список
    компаний по фильтрам
    """
    # slug_company = request.GET.get('slug')
    subdomain = request.GET.get('subdomain')
    print(subdomain)
    if not subdomain:
        try:
            subdomain = request.headers['Referer'].split('//')[1].split('.')[0]
        except:
            subdomain = None

    subcategory = request.GET.get('subcategory')
    brands = request.GET.get('brands')
    servicesslug = request.GET.get('servicesslug')

    courier_departure = bool(request.GET.get('courier_departure'))
    master_departure = bool(request.GET.get('master_departure'))
    free_diagnostics = bool(request.GET.get('free_diagnostics'))
    quick_repair = bool(request.GET.get('quick_repair'))
    pay_after_repair = bool(request.GET.get('pay_after_repair'))
    own_warehouse = bool(request.GET.get('own_warehouse'))
    free_parking = bool(request.GET.get('free_parking'))
    fix_price = bool(request.GET.get('fix_price'))
    cash_pay = bool(request.GET.get('cash_pay'))
    card_pay = bool(request.GET.get('card_pay'))

    # is_promo = bool(request.GET.get('is_promo'))
    # promo    = request.GET.get('promo')

    query = request.GET.dict()

    query_filter = Q()
    if len(query) > 2:
        if courier_departure:
            query_filter &= Q(courier_departure=True)
        if master_departure:
            query_filter &= Q(master_departure=True)
        if free_diagnostics:
            query_filter &= Q(free_diagnostics=True)
        if quick_repair:
            query_filter &= Q(quick_repair=True)
        if pay_after_repair:
            query_filter &= Q(pay_after_repair=True)
        if own_warehouse:
            query_filter &= Q(own_warehouse=True)
        if free_parking:
            query_filter &= Q(free_parking=True)
        if fix_price:
            query_filter &= Q(fix_price=True)
        if cash_pay:
            query_filter &= Q(cash_pay=True)
        if card_pay:
            query_filter &= Q(card_pay=True)
        # if is_promo:
        #     query_filter &= Q(is_promo=True)
        #     query_filter &= Q(promo=int(promo))
        if subdomain:
            if subcategory:
                queryset = Company.objects.filter(categories__slug=subcategory).filter(
                    query_filter,
                    city__subdomain__name=subdomain
                ).distinct()
                if queryset.count() == 0:
                    child_category = Category.objects.get(slug=subcategory)
                    parent_category = Category.objects.get(
                        id=child_category.parent_category_id)
                    categories = Category.objects.filter(
                        parent_category=parent_category)
                    queryset = Company.objects.filter(categories__in=categories).filter(
                        query_filter,
                        city__subdomain__name=subdomain
                    ).distinct()
            elif brands:
                queryset = Company.objects.filter(brands__slug=brands).filter(
                    query_filter,
                    city__subdomain__name=subdomain
                )
            else:
                queryset = Company.objects.filter(
                    query_filter,
                    city__subdomain__name=subdomain
                ).distinct()
        else:
            queryset = Company.objects.filter(
                query_filter,
                city__subdomain__name=subdomain
            ).distinct()
    else:
        if subdomain:
            if subcategory:

                queryset = Company.objects.filter(
                    categories__slug=subcategory
                ).filter(
                    city__subdomain__name=subdomain
                ).distinct().order_by('-is_promo', 'promo')
            elif brands:
                queryset = Company.objects.filter(
                    brands__slug=brands
                ).filter(
                    city__subdomain__name=subdomain
                ).order_by('-is_promo', 'promo')
            elif servicesslug:
                queryset = Company.objects.filter(
                    services__slug=servicesslug
                ).filter(
                    city__subdomain__name=subdomain
                ).order_by('-is_promo', 'promo')
            else:
                queryset = Company.objects.filter(
                    city__subdomain__name=subdomain
                ).order_by('-is_promo', 'promo')
        else:
            queryset = Company.objects.filter(
                city__subdomain__name=subdomain
            ).order_by('-is_promo', 'promo')

    # list_categories = []

    paginator = CustomPaginator()
    context = paginator.paginate_queryset(queryset, request)
    serializer = CompanySerializer(context, many=True)
    # categories_serialazer = CategorySerializer(list_categories[:20], many=True)
    return paginator.get_paginated_response(
        {
            'companies': serializer.data,
            'categories_important': []
        }
    )


@api_view(['GET'])
def get_search_company(request, *args, **kwargs):
    """
    Поиск компаний по полям {name},{brands},{category},{subcategory}
    """
    search = request.GET.get('search')
    city = request.GET.get('city')
    qty = int(request.GET.get('qty') or 10)
    companies = []

    if search:
        split_query = search.split(' ')
        query_search_category = None
        if len(split_query) > 1:
            print(type(split_query))
            if 'ремонт' in split_query:
                query_search_category = 1
                split_query.remove('ремонт')
                search = ' '.join(split_query)

            if 'Ремонт' in split_query:
                query_search_category = 1
                split_query.remove('Ремонт')
                search = ' '.join(split_query)

        if query_search_category:
            companies = Company.objects.filter(city__name=city).filter(
                Q(categories__declension_one_p__istartswith=search)
            ) .prefetch_related(
                Prefetch(
                    'categories',
                    queryset=Category.objects.filter(
                        declension_one_p__istartswith=search
                    )
                )
            ).distinct()[:qty]
        else:
            companies = Company.objects.filter(city__name=city).filter(
                # Q(name__icontains=search) |
                # Q(brands__name__istartswith=search) |
                Q(categories__declension_one_p__istartswith=search)
                | Q(categories__name__istartswith=search
                    )).prefetch_related(
                Prefetch(
                    'categories',
                    queryset=Category.objects.filter(
                        name__istartswith=search
                    )
                )
            ).distinct()[:qty]

    serializer = CompanySearchSerializer(companies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_search_slugcategory(request, *args, **kwargs):
    search = request.GET.get('search')
    if search:
        query_search_category = None
        split_query = search.split(' ')
        query_search_category = None
        if len(split_query) > 1:
            print(type(split_query))
            if 'ремонт' in split_query:
                query_search_category = 1
                split_query.remove('ремонт')
                search = ' '.join(split_query)

            if 'Ремонт' in split_query:
                query_search_category = 1
                split_query.remove('Ремонт')
                search = ' '.join(split_query)
    if query_search_category:
        queryset = Category.objects.filter(
            declension_one_p__istartswith=search
        )
    else:
        queryset = Category.objects.filter(
            name__istartswith=search
        )
    serializer = CategorySerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user_companies(request):
    qty = int(request.GET.get('qty') or 10)
    queryset = Company.objects.filter(
        author=request.user).order_by('-id')[:qty]
    serializer = CompanySerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_or_reset_logo_company(request, pk, *args, **kwargs):
    """
    Сохранение аватара пользователя
    """
    company = Company.objects.get(id=pk)
    company.logo = request.data.get('logo_company')
    company.save()
    return Response({'message': 'ok'})


@api_view(['DELETE'])
def delete_logo_company(request, pk, *args, **kwargs):
    """
    Удаление аватара пользователя
    """
    company = Company.objects.get(id=pk)
    company.logo.storage.delete(company.logo.name)
    company.logo = ''
    company.save()
    return Response({'message': 'ok'})
