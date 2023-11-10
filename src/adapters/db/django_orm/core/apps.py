import os

from django.apps import AppConfig


class CoreConfig(AppConfig):
    cwd = os.path.split(os.getcwd())
    BASE_DJANGO_APP_PATH = 'src.adapters.db.django_orm.'
    default_auto_field = 'django.db.models.BigAutoField'
    name = BASE_DJANGO_APP_PATH + 'core'