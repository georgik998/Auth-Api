#   ** code by George **
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from pydantic_settings import BaseSettings

from typing import Callable

from src.infra.logi import logger

from src.config import api_settings
from src.routers import router


async def startup():
    logger.info(f'API STARTED WORK {api_settings.API_HOST}')



async def shutdown():
    logger.info('API FINISHED WORK')


def get_application(
        startup_function: Callable,
        shutdown_function: Callable,
        settings: BaseSettings,
        main_router: APIRouter
) -> FastAPI:
    app = FastAPI(
        docs_url=settings.API_DOCS_URL,
        title=settings.TITLE,
        description=settings.DESCRIPTION
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            'http://localhost'
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", startup_function)
    app.add_event_handler("shutdown", shutdown_function)

    app.include_router(
        router=main_router,
        prefix=settings.BASE_PREFIX
    )
    return app


app = get_application(
    startup_function=startup,
    shutdown_function=shutdown,
    settings=api_settings,
    main_router=router
)
host = api_settings.API_HOST
port = api_settings.API_PORT
