"""
WSGI config for db project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
BASE_DJANGO_APP_PATH = 'src.adapters.db.django_orm.'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', {BASE_DJANGO_APP_PATH} + 'db.settings')

application = get_wsgi_application()
