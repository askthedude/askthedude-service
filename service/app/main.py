from fastapi import FastAPI
import web.controller as router

app = FastAPI(debug=True)

app.include_router(router.router, prefix="/api")