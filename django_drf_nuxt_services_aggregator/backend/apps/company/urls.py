from django.urls import path, include

from apps.company.views import (
    brand,
    category,
    company,
    point,
    company_images
)

urlpatterns = [
    # Companies
    path('companies/', include([
        path('', company.get_list_company, name='get_company_all'),
        path('count/', company.get_count_home, name='get_count_home'),
        path('search/', company.get_search_company, name='get_search_company'),
        path('search-slug/', company.get_search_slugcategory, name='get_search_slugcategory'),
        path('list-dev/', company.CompanyModelViewSet.as_view({'get': 'list'}), name='list'),
        path('create/', company.CompanyModelViewSet.as_view({'post': 'create'}), name='create_company'),
        path('update/<int:pk>/', company.CompanyModelViewSet.as_view({'put': 'update'}), name='update_company'),
        path('<int:pk>/', company.CompanyModelViewSet.as_view({'get': 'retrieve'}), name='get_company'),
        path('profile/<int:pk>/', company.CompanyModelViewSet.as_view({'get': 'get_company_for_profile'}), name='get_company'),
        path('company/<str:slug>/', company.CompanyModelViewSet.as_view({'get': 'get_slug'}), name='get_slug'),
        path('delete/<int:pk>/', company.CompanyModelViewSet.as_view({'delete': 'destroy'}), name='delete'),
        path('partial/<int:pk>/', company.CompanyModelViewSet.as_view({'patch': 'partial_update'}), name='update_point'),
        path('user-companies/', company.get_user_companies, name='get_user_companies'),
        path('add-logo/<int:pk>/', company.add_or_reset_logo_company, name='add_or_reset_logo_company'),
        path('delete-logo/<int:pk>/', company.delete_logo_company, name='delete_logo_company'),

    ])),

    # Brands
    path('brands/', include([
        path('', brand.BrandViewSet.as_view({'get': 'list'}), name='get_brands_all'),
        path('<int:pk>/', brand.BrandViewSet.as_view({'get': 'retrieve'}), name='get_brand'),
         path('letter/<str:letter>/', brand.BrandViewSet.as_view({'get': 'get_brand_letter'}), name='get_brand_letter'),
        path('search/', brand.get_brand_search, name='get_brand_search'),
        path('<str:slug>/', brand.BrandViewSet.as_view({'get': 'get_brand_by_slug'}), name='get_brand_by_slug'),
    ])),

    # Categories get_category_search
    path('categories/', include([
        path('', category.CategoryViewSet.as_view({'get': 'list'}), name='get_categories_all'),
        path('<int:pk>/', category.CategoryViewSet.as_view({'get': 'retrieve'}), name='get_category'),
        path('search/', category.get_category_search, name='get_category_search'),
        path('<str:slug>/', category.CategoryViewSet.as_view({'get': 'get_comany_by_slug'}), name='get_comany_by_slug'),
        path('slug/<str:name>/', category.CategoryViewSet.as_view({'get': 'retrieve_name_for_slug'}), name='retrieve_name_for_slug'),
    ])),

    # Points
    path('points/', include([
        path('', point.PointModelViewSet.as_view({'get': 'list'}), name='get_point_all'),
        path('create/', point.PointModelViewSet.as_view({'post': 'create'}), name='create_point'),
        path('update/<int:pk>/', point.PointModelViewSet.as_view({'put': 'update'}), name='update_point'),
        path('<int:pk>/', point.PointModelViewSet.as_view({'get': 'retrieve'}), name='get_point'),
        path('delete/<int:pk>/', point.PointModelViewSet.as_view({'delete': 'destroy'}), name='delete'),
    ])),

    # company images
    path('companies/images/', include([
        path('create/', company_images.CompanyImagesModelViewSet.as_view({'post': 'create'}), name='create_point'),
        path('create/<int:company_id>/', company_images.CompanyImagesModelViewSet.as_view({'post': 'create_from_company'}), name='create_point'),
        path('delete/<int:pk>/', company_images.CompanyImagesModelViewSet.as_view({'delete': 'destroy'}), name='delete'),
    ])),
]
