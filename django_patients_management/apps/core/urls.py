from django.urls import path, include

from apps.core.views import (
    HomepageView,
)


urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
]
