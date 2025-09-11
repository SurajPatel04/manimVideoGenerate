from fastapi import (
    APIRouter, 
    status, 
    HTTPException,
    Depends
)
from app.schema.manimGenerationSchema import MainmUserModel
from app.services.manim import call_graph
# from app.services.task import call_graph
from fastapi.responses import StreamingResponse
from app.utils.auth import getCurrentUser
from celery.result import AsyncResult
from app.core.queue import taskQueue
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


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def generate(query: MainmUserModel, userId: int=Depends(getCurrentUser)):
    
    task = call_graph.apply_async(args=[query.userQuery,userId.id,query.quality, query.format])
    return {"task_id": task.id}


@router.get("/result/{task_id}")
async def get_result(task_id: str, userId: int = Depends(getCurrentUser)):
    result = AsyncResult(task_id, app=taskQueue)
    
    if result.state == 'PROGRESS':
        return {
            "status": "in_progress",
            "state": result.state,
            "current_stage": result.info.get('current_stage'),
            "progress": result.info.get('progress'),
            "details": result.info.get('details'),
            "timestamp": result.info.get('timestamp')
        }
    elif result.state == 'SUCCESS':
        return {
            "status": "completed",
            "state": result.state,
            "data": result.result
        }
    elif result.state == 'FAILURE':
        return {
            "status": "failed",
            "state": result.state,
            "error": str(result.info)
        }
    else:
        return {
            "status": "pending",
            "state": result.state
        }