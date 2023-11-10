"""
ASGI config for db project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""


import os

from django.core.asgi import get_asgi_application
BASE_DJANGO_APP_PATH = 'src.adapters.db.django_orm.'
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', f'{BASE_DJANGO_APP_PATH}db.settings'
)

application = get_asgi_application()
