from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),

    path('api/v1/', include([
        path('users/', include('apps.users.urls')),
        path('blog/', include('apps.blog.urls')),
        path('services/', include('apps.services.urls')),
        path('', include('apps.cities.urls')),
        path('', include('apps.company.urls')),
        path('email/', include('apps.email_aplications.urls')),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
