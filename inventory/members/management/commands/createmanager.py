from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from members.models import User

class Command(BaseCommand):
    help = 'Creates a new manager user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the new manager')
        parser.add_argument('email', type=str, help='Email for the new manager')
        parser.add_argument('password', type=str, help='Password for the new manager')
        parser.add_argument('--first_name', type=str, help='First name for the new manager')
        parser.add_argument('--last_name', type=str, help='Last name for the new manager')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']
        first_name = kwargs.get('first_name', '')
        last_name = kwargs.get('last_name', '')

        UserModel = get_user_model()
        
        # Check if the user already exists
        if UserModel.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User with username "{username}" already exists'))
            return
        
        if UserModel.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f'User with email "{email}" already exists'))
            return
        
        # Create the user with manager role
        user = UserModel.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            role=User.Role.MANAGER,
            is_staff=False,
            is_superuser=False,
            is_active=True
        )
        
        self.stdout.write(self.style.SUCCESS(f'Manager user "{username}" created successfully!')) 