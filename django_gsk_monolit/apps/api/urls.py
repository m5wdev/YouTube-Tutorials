from django.urls import path, include

from apps.api.views import (
    api_sites_all,
    api_object_sites_info,
    api_site_info,

    api_object_commercial_sites_info,

    api_object_gallery,
    api_mortgage_offer,
)


app_name = 'api'

urlpatterns = [
    path('api/', include([
        # api:sites
        path('sites/', include(([
            # api:sites:all
            path('all/', api_sites_all, name='all'),
        ], app_name), namespace='sites')),

        # api:site
        path('site/', include(([
            # api:site:info
            path('<int:site_id>/info/', api_site_info, name='info'),
        ], app_name), namespace='site')),

        # api:objects-summary-info
        # path('objects-summary-info/', api_objects_summary_info, name="objects-summary-info"),

        # api:object
        path('object/', include(([
            # api:object:sites-info
            path('<int:object_id>/sites-info/', api_object_sites_info, name='sites-info'),

            # api:object:gallery
            path('gallery/<int:gallery_id>/', api_object_gallery, name='gallery'),
        ], app_name), namespace='object')),

        # api:object-commercial
        path('object-commercial/', include(([
            # api:object-commercial:sites-info
            path('<int:object_commercial_id>/sites-info/', api_object_commercial_sites_info, name='sites-info'),
        ], app_name), namespace='object-commercial')),

        # api:mortgage
        path('mortgage/', include(([
            # api:mortgage:offer
            path('offer/<int:offer_id>/', api_mortgage_offer, name='offer'),
        ], app_name), namespace='mortgage')),
    ])),
]
