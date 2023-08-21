from django.urls import path, include

from apps.core.views import (
    HomepageView,

    search_results_view,
)


search_patterns = ([
    path('search-results/', search_results_view, name='results'),
], 'search')

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),

    path('', include(search_patterns)),
]