import multiprocessing

import uvicorn
from fastapi import (
    FastAPI,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status,
    Request,
    Form,
)
from fastapi.responses import JSONResponse
from dependencies import container # noqa
from src.adapters.authentication_provider.authentication import (
    Authenticate,
    ServiceAuthorize,
)
from src.config import service_config as service_config
from src.frameworks.api.configs.fastapi_doc import (
    fastapi_information,
    fastapi_tags_metadata,
)
from src.utils.basic_logger import simple_logger as logger


class FastAPIConfig:
    information = fastapi_information
    tags_metadata = fastapi_tags_metadata

    def __init__(self):
        self.information = fastapi_information
        self.tags_metadata = fastapi_tags_metadata


class APIEndpoint:
    def __init__(
        self,
        auth: Authenticate,
        authorize: ServiceAuthorize,
        configs: FastAPIConfig,
        logger: logger,
    ) -> None:
        self.auth = auth
        self.authorize = authorize
        self.configs = configs
        self.logger = logger
        self.rest_api_app = None
        self.create_rest_api_app(self.configs.information, self.configs.tags_metadata)
        self.create_rest_api_route()

    def create_rest_api_app(self, information, tags_metadata) -> None:
        self.rest_api_app = FastAPI(**information, openapi_tags=tags_metadata)

    def start_rest_api_app(self) -> None:
        self.logger.info("Starting API Endpoint...")
        self.rest_api_process = multiprocessing.Process(
            target=uvicorn.run,
            kwargs={
                "app": self.rest_api_app,
                "host": service_config.SERVICE_HOST,
                "port": int(service_config.SERVICE_PORT),
            },
        ).start()

    def create_rest_api_route(self):
        if self.rest_api_app is None:
            return

        @self.rest_api_app.get(
            "/",
            tags=["Main"],
            responses={
                status.HTTP_200_OK: {"description": "Success"},
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "Error in authenticating user due to invalid token."
                },
            },
        )
        async def main(request: Request):
            """Check the Status of the Service."""
            return JSONResponse(
                status_code=status.HTTP_200_OK, content={"message": "Success"}
            )
        

        @self.rest_api_app.get(
            "/service",
            tags=["Main"],
            responses={
                status.HTTP_200_OK: {"description": "Success"},
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "Error in authenticating user due to invalid token."
                },
            },
        )
        async def service(
            token: str = Depends(self.auth.oauth2_scheme),
            has_permission: bool = Depends(self.authorize),
        ):
            """Check the Status of the Service."""
            return JSONResponse(
                status_code=status.HTTP_200_OK, content={"message": "Success"}
            )
