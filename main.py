from fastapi import FastAPI
from app.routers.user import router as users_router

app = FastAPI()


app.include_router(users_router)