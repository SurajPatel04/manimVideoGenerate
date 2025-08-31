from fastapi import FastAPI

from app.router import mainmGeneration

app = FastAPI()

app.include_router(mainmGeneration.router)

