"""
WSGI config for travel2india project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel2india.settings')

django.setup()

# Run collectstatic on startup
try:
    print("Running collectstatic on startup...")
    call_command('collectstatic', '--noinput')
except Exception as e:
    print(f"Error running collectstatic: {e}")

# Run database migrations on startup
try:
    print("Running migrate on startup...")
    call_command('migrate', '--noinput')
except Exception as e:
    print(f"Error running migrate: {e}")

application = get_wsgi_application()
