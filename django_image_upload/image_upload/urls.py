from django.urls import path, include

from .views import (
    images_homepage_view,
    image_upload_view,
    image_sizing_view
)


app_name = 'image'

urlpatterns = [
    path('', images_homepage_view, name='homepage'),
    path('image/', include([
        path('upload/', image_upload_view, name='upload'),
        path('sizing/', image_sizing_view, name='sizing'),
    ]))
]