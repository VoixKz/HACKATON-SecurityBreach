from django.core.management.base import BaseCommand
from parsingVulnerabilities.parsing import main

class Command(BaseCommand):
    help = 'Fetch the latest vulnerabilities for POC from sploitus.com'

    def handle(self, *args, **kwargs):
        main('POC')
        self.stdout.write(self.style.SUCCESS('Successfully started fetching vulnerabilities for POC'))