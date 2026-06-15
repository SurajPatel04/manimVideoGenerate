from app.router import (
    mainmGeneration, 
    userRouter
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.core.db import init_db
from app.utils.auth import getCurrentUser
from app.exceptions import UserAlreadyVerifiedException, UserNotFoundException
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from starlette.middleware.sessions import SessionMiddleware
from app.config.config import Config

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(app)
    try:
        yield
    finally:
        await app.state.mongo_client.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key=Config.SECRET_KEY
)

@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)}
    )

@app.exception_handler(UserAlreadyVerifiedException)
async def user_already_verified_exception_handler(request: Request, exc: UserAlreadyVerifiedException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": str(exc)}
    )

origins = [
    "http://localhost:5173",
    "https://video.surajpatel.dev",
    "www.video.surajpatel.dev"
]

assets_path = Path(__file__).resolve().parent / "assets"
app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(mainmGeneration.router)
app.include_router(userRouter.router)
