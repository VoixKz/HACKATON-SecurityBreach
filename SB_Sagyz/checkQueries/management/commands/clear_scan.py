from django.core.management.base import BaseCommand
from checkQueries.models import Query, ScanHistory

class Command(BaseCommand):
    help = 'Удаляет все записи в таблицах Query и ScanHistory'

    def handle(self, *args, **kwargs):
        Query.objects.all().delete()
        ScanHistory.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Все записи в таблицах Query и ScanHistory были удалены'))