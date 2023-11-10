#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import django

BASE_DJANGO_APP_PATH = "src.adapters.db.django_orm."


def config_django():
    from src.adapters.db.django_orm.db import asgi

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", f"{BASE_DJANGO_APP_PATH}db.settings"
    )
    os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
    django.setup()


def main():
    """Run administrative tasks."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", f"{BASE_DJANGO_APP_PATH}db.settings"
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
