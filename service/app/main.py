from fastapi import FastAPI

import web.project_router as project_router
import web.user_router as user_router
import web.auth_router as auth_router
import web.technology_router as tech_router

from fastapi.middleware.cors import CORSMiddleware

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


app.include_router(project_router.router, prefix="/api")
app.include_router(user_router.router, prefix="/api")
app.include_router(auth_router.router, prefix="/api")
app.include_router(tech_router.router, prefix="/api")