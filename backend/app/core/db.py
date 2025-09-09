from pymongo import AsyncMongoClient
from dotenv import load_dotenv
from beanie import init_beanie
from app.models.User import User
import os
load_dotenv()

async def init_db(app):
    client = AsyncMongoClient(os.getenv("MONGODB_URL"))
    await init_beanie(database=client["manimVideoGenerator"], document_models=[User])
    app.state.mongo_client = client