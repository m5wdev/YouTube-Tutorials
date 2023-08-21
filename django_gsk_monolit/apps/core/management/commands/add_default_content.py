""" README https://docs.djangoproject.com/en/dev/howto/custom-management-commands/ """

from django.core.management.base import BaseCommand, CommandError
from apps.core.classes.add_default_content import AddDefaultContent


class Command(BaseCommand):
    help = 'Create or Update Default content'

    def handle(self, *args, **options):
        add_default_content = AddDefaultContent()
        add_default_content.addContent()

        self.stdout.write(self.style.SUCCESS('Default content Created'))
        # self.stdout.write(self.style.ERROR('Error message'))
