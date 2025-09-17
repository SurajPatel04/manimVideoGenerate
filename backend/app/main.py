from app.router import (
    mainmGeneration, 
    userRouter
)
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.core.db import init_db
from app.utils.auth import getCurrentUser

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(app)
    try:
        yield
    finally:
        app.state.mongo_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(mainmGeneration.router)
app.include_router(userRouter.router)

