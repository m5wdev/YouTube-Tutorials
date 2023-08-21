from django.urls import path

from .views import create_company_application, create_company_abuse, create_repair_application


urlpatterns = [
    path('create-company-application/', create_company_application, name='create_company_application'),
    path('create-company-abuse/', create_company_abuse, name='create_company_abuse'),
    path('create-repair-application/', create_repair_application, name='create_repair_application'),
]
