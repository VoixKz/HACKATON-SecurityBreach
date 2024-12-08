from django.core.management.base import BaseCommand
from botScanner.bosfor_operator import check_ip_for_cve

class Command(BaseCommand):
    help = 'Check an IP for a given CVE tag'

    def add_arguments(self, parser):
        parser.add_argument('target_ip', type=str, help='Target IP address to check')
        parser.add_argument('cve_tag', type=str, help='CVE tag to check against')

    def handle(self, *args, **kwargs):
        target_ip = kwargs['target_ip']
        cve_tag = kwargs['cve_tag']
        try:
            results = check_ip_for_cve(target_ip, cve_tag)
            self.stdout.write(self.style.SUCCESS(f'Results for IP {target_ip} and {cve_tag}: {results}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))