from django.core.management.base import BaseCommand
from rest_framework_simplejwt.tokens import RefreshToken
from authApp.models import CustomUser

class Command(BaseCommand):
    help = 'Obtain a token for a user'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email of the user')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        try:
            user = CustomUser.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            self.stdout.write(self.style.SUCCESS(f'Access Token: {refresh.access_token}'))
            self.stdout.write(self.style.SUCCESS(f'Refresh Token: {refresh}'))
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR('User does not exist'))