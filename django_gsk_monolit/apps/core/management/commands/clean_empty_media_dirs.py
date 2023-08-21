""" README https://docs.djangoproject.com/en/dev/howto/custom-management-commands/ """

from django.core.management.base import BaseCommand, CommandError

from apps.core.classes.clean_media import CleanMedia


class Command(BaseCommand):
    help = 'Create Default content'

    def handle(self, *args, **options):
        cleanMedia = CleanMedia()
        # Delete empty dirs in /media/
        cleanMedia.deleteEmptyDirsRecusive()
        self.stdout.write(self.style.SUCCESS('All empty dirs in /media/ has been cleaned'))
