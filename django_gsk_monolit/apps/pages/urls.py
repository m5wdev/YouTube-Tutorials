from django.urls import path, include

from apps.pages.views import PageDetailView


app_name = 'pages'

urlpatterns = [
    path('p/', include([
        path('<slug:slug>/', PageDetailView.as_view(), name='detail'),
    ])),
]
