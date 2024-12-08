from django.core.management.base import BaseCommand
from botScanner.bosfor_operator import generate_yaml_template

class Command(BaseCommand):
    help = 'Generate a YAML template for a given CVE tag'

    def add_arguments(self, parser):
        parser.add_argument('cve_tag', type=str, help='CVE tag to generate YAML template for')

    def handle(self, *args, **kwargs):
        cve_tag = kwargs['cve_tag']
        try:
            generate_yaml_template(cve_tag)
            self.stdout.write(self.style.SUCCESS(f'YAML template generated for CVE: {cve_tag}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))