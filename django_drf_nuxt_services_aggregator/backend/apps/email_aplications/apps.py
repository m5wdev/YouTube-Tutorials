from django.apps import AppConfig


class EmailAplicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.email_aplications'
    verbose_name = 'Email заявки'
    label = 'email_aplications'