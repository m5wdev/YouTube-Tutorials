from django.apps import AppConfig


class CompanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.company'
    verbose_name = 'Компании и мастерские'
    label = 'company'
