from django.core.management.base import BaseCommand
from botScanner.data_crawler import crawl_shodan

class Command(BaseCommand):
    help = 'Get all information from Shodan for a given IP address'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='IP address to get information for')

    def handle(self, *args, **kwargs):
        ip_address = kwargs['ip_address']
        try:
            result = crawl_shodan(ip_address)
            if result:
                self.stdout.write(self.style.SUCCESS(f'Information for IP {ip_address}: {result}'))
            else:
                self.stdout.write(self.style.ERROR(f'No information found for IP {ip_address}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))