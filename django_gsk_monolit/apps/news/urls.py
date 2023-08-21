from django.urls import path, include

from apps.news.views import (
    NewsListView,
    NewsDetailView,

    ActionsListView,
    ActionsDetailView,
)


app_name = 'news'

urlpatterns = [
    path('news/', include([
        path('', NewsListView.as_view(), name='list'),
        path('<int:pk>/', NewsDetailView.as_view(), name='detail'),
    ])),

    path('actions/', include(([
        path('', ActionsListView.as_view(), name='list'),
        path('<int:pk>/', ActionsDetailView.as_view(), name='detail'),
    ], app_name), namespace='actions')),
]
