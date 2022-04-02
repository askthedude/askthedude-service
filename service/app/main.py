from fastapi import FastAPI
import web.controller as router
from storage.database import init_db

app = FastAPI(debug=True)


@app.on_event("startup")
async def init():
    await init_db()

# @app.middleware("http")
# async def logger_middleware(request: Request, call_next):
#     # logger.info(f"Got HTTP {request.method} Request on URI: {request.url.path}.")
#     response = await call_next(request)
#     return response

app.include_router(router.router, prefix="/api")