from fastapi import FastAPI
import web.user as user_router


app = FastAPI()

app.include_router(user_router.router)