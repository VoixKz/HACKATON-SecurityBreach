from django.core.management.base import BaseCommand
from botScanner.data_crawler import scrap_data_ip

class Command(BaseCommand):
    help = 'Scrap data for a given IP address'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='IP address to scrap data for')

    def handle(self, *args, **kwargs):
        ip_address = kwargs['ip_address']
        try:
            result = scrap_data_ip(ip_address)
            self.stdout.write(self.style.SUCCESS(f'Scraped Data: {result}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))