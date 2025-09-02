from fastapi import APIRouter, status, HTTPException
from app.schema.manimGenerationSchema import MainmUserModel
from app.services.manim import call_graph
from fastapi.responses import StreamingResponse
import json

router = APIRouter(
    prefix="/api/manimGeneration"
)


@router.get("/")
def hello():
    return {"data":"hello World"}

@router.post("/generate")
async def generateManimVideo(query: MainmUserModel):
    async def event_generator():
        async for event in call_graph(query.userQuery):
            # Convert each graph event into SSE format
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
