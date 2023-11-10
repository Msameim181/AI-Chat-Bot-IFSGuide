from dotenv import dotenv_values
from collections import namedtuple

__all__ = [
    "service_config",
    "database_config",
]



_service = dotenv_values("./src/config_files/service.env")
service_config = namedtuple("serviceConfig", _service)(
    **_service
)

_database = dotenv_values("./src/config_files/database.env")
database_config = namedtuple("DatabaseConfig", _database)(**_database)
