from fastapi import (
    APIRouter, 
    status, 
    HTTPException
)
from app.schema.manimGenerationSchema import MainmUserModel
from app.services.manim import call_graph
# from app.services.task import call_graph
from fastapi.responses import StreamingResponse
import json

router = APIRouter(
    prefix="/api/manimGeneration"
)


@router.get("/")
def hello():
    return {"data":"hello World"}

# @router.post("/generate", status_code=status.HTTP_201_CREATED)
# async def generateManimVideo(query: MainmUserModel):
#     async def event_generator():
#         async for event in call_graph(query.userQuery):
#             yield f"data: {json.dumps(event)}\n\n"
#         yield "event: end\ndata: [DONE]\n\n"
#     return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/")
async def generate(query: MainmUserModel):
    """
    This endpoint now correctly queues the background task.
    It receives a query, calls `.apply_async()` on the imported task,
    and immediately returns a task ID to the client.
    """
    # Use .apply_async to send the task to the Celery queue.
    # The `args` tuple must match the arguments of your task function.
    task = call_graph.apply_async(args=[query.userQuery])
    
    # Return the task_id so the client can check the status later.
    return {"task_id": task.id}