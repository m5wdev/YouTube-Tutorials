from django.urls import path, include

from apps.realty.views import (
    ObjectListView,
    ObjectDetailView,

    ObjectSiteListView,
    ObjectSiteDetailView,
    ObjectSiteDetailViewPDF,

    ObjectCommercialListView,
    ObjectCommercialDetailView,

    ObjectCommercialSiteListView,
    ObjectCommercialSiteDetailView,
    ObjectCommercialSiteDetailViewPDF,
)


objects_patterns = ([
    path('', ObjectListView.as_view(), name='list'),
    path('<slug:slug>/', ObjectDetailView.as_view(), name='detail')
], 'objects')

sites_patterns = ([
    path('', ObjectSiteListView.as_view(), name='list'),
    path('<int:pk>/', ObjectSiteDetailView.as_view(), name='detail'),
    path('<int:pk>/pdf/', ObjectSiteDetailViewPDF.as_view(), name='pdf'),
], 'sites')

objects_commercial_patterns = ([
    path('', ObjectCommercialListView.as_view(), name='list'),
    path('<slug:slug>/', ObjectCommercialDetailView.as_view(), name='detail'),
], 'objects-commercial')

sites_commercial_patterns = ([
    path('', ObjectCommercialSiteListView.as_view(), name='list'),
    path('<int:pk>/', ObjectCommercialSiteDetailView.as_view(), name='detail'),
    path('<int:pk>/pdf/', ObjectCommercialSiteDetailViewPDF.as_view(), name='pdf'),
], 'sites-commercial')


urlpatterns = [
    path('objects/', include(objects_patterns)),
    path('sites/', include(sites_patterns)),

    path('objects-commercial/', include(objects_commercial_patterns)),
    path('sites-commercial/', include(sites_commercial_patterns)),
]
