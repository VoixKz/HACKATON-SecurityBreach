from django.core.management.base import BaseCommand
from rest_framework_simplejwt.tokens import RefreshToken

class Command(BaseCommand):
    help = 'Refresh a token'

    def add_arguments(self, parser):
        parser.add_argument('refresh_token', type=str, help='Refresh token')

    def handle(self, *args, **kwargs):
        refresh_token = kwargs['refresh_token']
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token
            self.stdout.write(self.style.SUCCESS(f'New Access Token: {new_access_token}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))