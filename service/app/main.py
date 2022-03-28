from fastapi import FastAPI
import web.controller as router

app = FastAPI()

app.include_router(router.router)