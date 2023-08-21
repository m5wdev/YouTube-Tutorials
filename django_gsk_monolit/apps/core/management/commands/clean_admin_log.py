from django.core.management.base import BaseCommand, CommandError

# https://stackoverflow.com/a/23521095/2891421
from django.contrib.admin.models import LogEntry


class Command(BaseCommand):
    help = 'Clean admin log entries from DB'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS( LogEntry.objects.all() ))
        LogEntry.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All log antries successfully removed!'))
