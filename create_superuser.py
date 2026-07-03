import os
import sys
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser(description='Create a Django superuser from environment variables or command-line arguments.')
    parser.add_argument('--username', help='Superuser username')
    parser.add_argument('--email', help='Superuser email address')
    parser.add_argument('--password', help='Superuser password')
    args = parser.parse_args()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.settings')

    import django
    django.setup()

    from django.contrib.auth import get_user_model

    User = get_user_model()

    username = args.username or os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = args.email or os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = args.password or os.environ.get('DJANGO_SUPERUSER_PASSWORD')

    if not username or not email or not password:
        print('Error: username, email, and password are required.')
        print('You can pass values via command-line arguments or environment variables:')
        print('  DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD')
        sys.exit(1)

    if User.objects.filter(username=username).exists():
        print(f'Superuser "{username}" already exists. No action taken.')
        sys.exit(0)

    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Created superuser "{username}" successfully.')
