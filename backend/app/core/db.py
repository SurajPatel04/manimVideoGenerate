from pymongo import AsyncMongoClient
from beanie import init_beanie
from app.models.User import Users
from app.models.RefreshToken import RefreshToken
from app.models.UserHistory import UsersHistory
from app.config import Config
import asyncio

# Global variable to store the client for workers
_worker_client = None

async def init_db(app):
    client = AsyncMongoClient(Config.MONGODB_URL)
    await init_beanie(
        database=client["manimVideoGenerator"], 
        document_models=[Users, RefreshToken,UsersHistory]
    )
    app.state.mongo_client = client

async def init_beanie_for_workers():
    """Initialize Beanie for Celery workers without FastAPI app context"""
    global _worker_client
    
    # Close existing client if it exists and was created in a different loop
    if _worker_client is not None:
        try:
            await _worker_client.close()
        except Exception:
            pass
    
    # Create new client in current event loop
    _worker_client = AsyncMongoClient(os.getenv("MONGODB_URL"))
    await init_beanie(
        database=_worker_client["manimVideoGenerator"], 
        document_models=[Users, RefreshToken, UsersHistory]
    )
    return _worker_client

async def close_worker_db():
    """Close the worker database connection"""
    global _worker_client
    if _worker_client is not None:
        await _worker_client.close()
        _worker_client = None