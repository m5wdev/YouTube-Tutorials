from django.apps import AppConfig


class CitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cities'
    verbose_name = 'Города, Метро'
    label = 'city'
