from django.urls import path, include

from .views import *

urlpatterns = [
    # Categories
        path('', CategoryServiceModelViewSet.as_view({'get': 'list'}), name='get_categories_all'),
        path('all-services-city/', get_all_services, name='get_all_services'),
        path('<int:pk>/', CategoryServiceModelViewSet.as_view({'get': 'retrieve'}), name='get_category'),
        path('company/<str:slug>/', CategoryServiceModelViewSet.as_view({'get': 'get_company_categories'}), name='get_company_categories'),
        path('city/<str:slug_city>/', CategoryServiceModelViewSet.as_view({'get': 'get_service_for_city'}), name='get_company_categories'),
        path('<str:slug_service>/', CategoryServiceModelViewSet.as_view({'get': 'get_service_name'}), name='get_service_name'),
]
