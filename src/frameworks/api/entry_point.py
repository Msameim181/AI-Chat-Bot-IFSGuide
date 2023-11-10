import json
import multiprocessing
import uvicorn
import jwt
from typing import Annotated, Union

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Request,
)
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from dependencies import container  # noqa
from src.config import service_config as service_config
from src.entities import User, RoleType, Interaction, Message
from src.frameworks.api.configs.fastapi_doc import (
    fastapi_information,
    fastapi_tags_metadata,
)
from src.frameworks.api.schemas.message import CreateMessage
from src.frameworks.api.schemas.user import UserSignup
from src.use_cases import UserUseCase, InteractionUseCase, MessageUseCase
from src.use_cases.exceptions import (
    UserNotAuthorized,
    InteractionNotFound,
    UserNotFound,
    AIFailedToRespond,
)
from src.utils.basic_logger import simple_logger as logger


class FastAPIConfig:
    information = fastapi_information
    tags_metadata = fastapi_tags_metadata

    def __init__(self):
        self.information = fastapi_information
        self.tags_metadata = fastapi_tags_metadata


class Auth:
    def __init__(self):
        self.oauth2_scheme = OAuth2PasswordBearer(
            tokenUrl="/login",
        )


class APIEndpoint:
    def __init__(
        self,
        auth: Auth,
        configs: FastAPIConfig,
        logger: logger,
        user_use_case: UserUseCase,
        interaction_use_case: InteractionUseCase,
        message_use_case: MessageUseCase,
    ) -> None:
        self.auth = auth
        self.configs = configs
        self.logger = logger
        self.user_use_case = user_use_case
        self.interaction_use_case = interaction_use_case
        self.message_use_case = message_use_case
        self.rest_api_app = None
        self.create_rest_api_app(self.configs.information, self.configs.tags_metadata)
        self.create_rest_api_route()

    def create_rest_api_app(self, information, tags_metadata) -> None:
        self.rest_api_app = FastAPI(**information, openapi_tags=tags_metadata)

    def start_rest_api_app(self, main_process: bool = False) -> None:
        self.logger.info("Starting API Endpoint...")
        if main_process:
            uvicorn.run(
                self.rest_api_app,
                host=service_config.SERVICE_HOST,
                port=int(service_config.SERVICE_PORT),
            )
        else:
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
            },
        )
        async def main(request: Request):
            """Check the Status of the Service."""
            # redirect to docs
            return RedirectResponse(url="/docs")

        @self.rest_api_app.post(
            "/signup",
            tags=["User"],
            responses={
                status.HTTP_200_OK: {"description": "Success"},
            },
        )
        async def signup(form_data: UserSignup):
            """Create a new user."""
            response = await self.user_use_case.add_new_user(
                User(
                    id=None,
                    name=form_data.name,
                    email=form_data.email,
                    password=form_data.password,
                )
            )
            if response is None:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"message": "Failed to create user"},
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Success, user created. Please login to continue."},
            )

        @self.rest_api_app.post(
            "/login",
            tags=["User"],
            responses={
                status.HTTP_200_OK: {"description": "Success"},
            },
        )
        async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
            try:
                response = await self.user_use_case.user_login(
                    form_data.username, form_data.password
                )
            except UserNotFound as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User not found, please sign up first. Error: {e}",
                )
            except UserNotAuthorized as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"User not authorized. Error: {e}",
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Internal server error. Error: {e}",
                )
            user_data = {
                "id": response.id,
                "name": response.name,
                "email": response.email,
                "is_verified": response.is_verified,
            }
            # create a token for the user with jwt
            token = jwt.encode(
                user_data, service_config.JWT_SECRET_KEY, algorithm="HS256"
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"access_token": token, "token_type": "bearer"},
            )

        @self.rest_api_app.get(
            "/service",
            tags=["AuthCheck"],
            responses={
                status.HTTP_200_OK: {"description": "Success"},
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "Error in authenticating user due to invalid token."
                },
            },
        )
        async def service(
            token: str = Depends(self.auth.oauth2_scheme),
        ):
            """Check the Status of the Service."""
            return JSONResponse(
                status_code=status.HTTP_200_OK, content={"message": "Success"}
            )

        @self.rest_api_app.post(
            "/interaction/create",
            tags=["Interaction"],
            responses={
                status.HTTP_200_OK: {"description": "Success"},
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "Error in authenticating user due to invalid token."
                },
            },
        )
        async def create_interaction(
            token: str = Depends(self.auth.oauth2_scheme),
        ):
            """Create a new interaction."""
            user_data = jwt.decode(
                token, service_config.JWT_SECRET_KEY, algorithms=["HS256"]
            )
            response = await self.interaction_use_case.add_new_interaction(
                Interaction(
                    id=None,
                    user_id=user_data["id"],
                )
            )
            if response is None:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"message": "Failed to create interaction"},
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success, interaction created.",
                    "interaction_id": response.id,
                },
            )

        @self.rest_api_app.get(
            "/interaction/fetch_all",
            tags=["Interaction"],
            responses={
                status.HTTP_200_OK: {"description": "Success"},
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "Error in authenticating user due to invalid token."
                },
            },
        )
        async def fetch_all_interactions(
            token: str = Depends(self.auth.oauth2_scheme),
        ):
            """Fetch all interactions for a user."""
            user_data = jwt.decode(
                token, service_config.JWT_SECRET_KEY, algorithms=["HS256"]
            )
            response = await self.interaction_use_case.retrieve_all(
                user_id=user_data["id"],
            )
            if response is None:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"message": "Failed to fetch interactions"},
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"interactions": json.dumps(response)},
            )

        @self.rest_api_app.post(
            "/message/create",
            tags=["Message"],
            responses={
                status.HTTP_200_OK: {"description": "Success"},
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "Error in authenticating user due to invalid token."
                },
            },
        )
        async def create_message(
            form_data: CreateMessage,
            token: str = Depends(self.auth.oauth2_scheme),
        ):
            """Create a new message in an interaction."""
            user_data = jwt.decode(
                token, service_config.JWT_SECRET_KEY, algorithms=["HS256"]
            )
            try:
                response = await self.message_use_case.add_new_message(
                    Message(
                        id=None,
                        interaction_id=form_data.interaction_id,
                        role=RoleType.HUMAN.value,
                        content=form_data.message,
                    ),
                    user_id=user_data["id"],
                    will_ai_respond=True,
                )
            except InteractionNotFound as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Interaction not found, please create an interaction first. Error: {e}",
                )
            except UserNotAuthorized as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"User not authorized. Error: {e}",
                )
            except AIFailedToRespond as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"AI failed to respond. Error: {e}",
                )
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "message": f"Failed to create and send a message. Error: {e}"
                    },
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"ai_response": response.content},
            )

        @self.rest_api_app.get(
            "/message/fetch_all/{interaction_id}",
            tags=["Message"],
            responses={
                status.HTTP_200_OK: {"description": "Success"},
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "Error in authenticating user due to invalid token."
                },
            },
        )
        async def fetch_all_messages(
            interaction_id: Union[int, str],
            token: str = Depends(self.auth.oauth2_scheme),
        ):
            """Fetch all messages for an interaction."""
            user_data = jwt.decode(
                token, service_config.JWT_SECRET_KEY, algorithms=["HS256"]
            )
            try:
                response = await self.message_use_case.retrieve_all(
                    interaction_id=interaction_id,
                    user_id=user_data["id"],
                )
            except InteractionNotFound as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Interaction not found, please create an interaction first. Error: {e}",
                )
            except UserNotAuthorized as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"User not authorized. Error: {e}",
                )
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "message": f"Failed to create and send a message. Error: {e}"
                    },
                )
            if response is None:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"message": "Failed to fetch messages"},
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"messages": json.dumps(response)},
            )
