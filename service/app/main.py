from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

import web.project_router as project_router
import web.user_router as user_router
import web.auth_router as auth_router
import web.technology_router as tech_router
import service.healthcheck_service as healthcheck_service

from fastapi.middleware.cors import CORSMiddleware

# CORS, and other basic security related stuff
origins = [
    "http://localhost",
    "http://localhost:8080",
    "*"
]


app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# api endpoints
app.include_router(project_router.router, prefix="/api")
app.include_router(user_router.router, prefix="/api")
app.include_router(auth_router.router, prefix="/api")
app.include_router(tech_router.router, prefix="/api")


# Healthcheck mechanisms for service and it's resources ( database, ..etc )
HEALTH_STATUSES = {
    "healthy": "GREEN",
    "kinda_healthy": "YELLOW",
    "unhealthy": "RED",
}


@app.get("/healthcheck")
async def healthcheck():
    res = await healthcheck_service.healthcheck()
    if res is None:
        return {"status": HEALTH_STATUSES['unhealthy']}
    else:
        return {"status": HEALTH_STATUSES['healthy']}


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print(e)
        return Response("Internal server error", status_code=500)

app.middleware('http')(catch_exceptions_middleware)