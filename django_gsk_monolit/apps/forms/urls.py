from django.urls import path, include
from .views import callback_form, mortgage_form, book_site_form


app_name = 'forms'

urlpatterns = [
    path('forms/', include([
        path('callback/', callback_form, name="callback"),
        path('mortgage/', mortgage_form, name="mortgage"),
        path('book-site/', book_site_form, name="book-site"),
    ])),
]
