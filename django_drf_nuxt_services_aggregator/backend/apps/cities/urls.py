from django.urls import path, include

from .views import (
                    CityViewSet,
                    MetroLineViewSet,
                    MetroStationViewSet,
                    get_city_name,
                    get_cities_search,
                    get_metro_city_search
                )

urlpatterns = [
    # Cities
    path('cities/', include([
        path('', CityViewSet.as_view({'get': 'list'}), name='get_cities'),
        path('<int:pk>/', CityViewSet.as_view({'get': 'retrieve'}), name='get_city'),
        path('metro/<int:id>/', CityViewSet.as_view({'get':'get_metro_in_city'}), name='get_metro_in_city'),
        path('search/', get_cities_search, name='get_cities_search'),
        path('name/', get_city_name, name='get_city_name'),
    ])),



    # MetroLine
    path('metro-line/', include([
        path('', MetroLineViewSet.as_view({'get': 'list'}), name='get_metroLines'),
        path('<int:pk>/', MetroLineViewSet.as_view({'get': 'retrieve'}), name='get_metroLine'),
    ])),


    # MetroStation
    path('metro-station/', include([
        path('', MetroStationViewSet.as_view({'get': 'list'}), name='get_metroLines'),
        path('search/', get_metro_city_search, name='get_metro_city_search'),
        path('<int:pk>/', MetroStationViewSet.as_view({'get': 'retrieve'}), name='get_metroLine'),
    ])),
]
