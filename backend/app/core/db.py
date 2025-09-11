from pymongo import AsyncMongoClient
from dotenv import load_dotenv
from beanie import init_beanie
from app.models.User import Users
from app.models.RefreshToken import RefreshToken
from app.models.UserHistory import UsersHistory
import os
load_dotenv()

async def init_db(app):
    client = AsyncMongoClient(os.getenv("MONGODB_URL"))
    await init_beanie(
        database=client["manimVideoGenerator"], 
        document_models=[Users, RefreshToken,UsersHistory]
    )
    app.state.mongo_client = client

async def init_beanie_for_workers():
    """Initialize Beanie for Celery workers without FastAPI app context"""
    client = AsyncMongoClient(os.getenv("MONGODB_URL"))
    await init_beanie(
        database=client["manimVideoGenerator"], 
        document_models=[Users, RefreshToken, UsersHistory]
    )
    return client