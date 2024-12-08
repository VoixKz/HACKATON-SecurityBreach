from django.core.management.base import BaseCommand
from parsingVulnerabilities.models import Exploit, Vulnerability

class Command(BaseCommand):
    help = 'Удаляет все записи в таблицах Exploit и Vulnerability'

    def handle(self, *args, **kwargs):
        Exploit.objects.all().delete()
        Vulnerability.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Все записи в таблицах Exploit и Vulnerability были удалены'))