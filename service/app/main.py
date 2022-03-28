
from fastapi import FastAPI
from starlette.requests import Request

import web.controller as router
from utils.log_config import LogConfig
from logging.config import dictConfig
import logging

dictConfig(LogConfig().dict())
app = FastAPI()

logger = logging.getLogger("WEBAPI")


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    logger.info(f"Got HTTP {request.method} Request on URI: {request.url.path}. {request.body()}.")
    response = await call_next(request)
    return response

app.include_router(router.router)