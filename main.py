import manage

manage.config_django()
from src import config_dependency_injection  # noqa

from dependencies import container  # noqa
from src.frameworks.api import APIEndpoint # noqa
from src.utils.basic_logger import simple_logger as logger # noqa
import asyncio # noqa


if __name__ == "__main__":
    container[logger].info("Starting AI-Chat-Bot-IFSGuide Service...")
    container[APIEndpoint].start_rest_api_app()

