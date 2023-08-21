""" README https://docs.djangoproject.com/en/dev/howto/custom-management-commands/ """

from django.core.management.base import BaseCommand, CommandError
from apps.core.classes.add_default_settings import AddDefaultSettings


class Command(BaseCommand):
    help = 'Create Default Settings'

    def handle(self, *args, **options):
        add_default_settings = AddDefaultSettings()
        add_default_settings.addSettings()

        self.stdout.write(self.style.SUCCESS('Default Settings Added!'))
        # self.stdout.write(self.style.ERROR('Error message'))