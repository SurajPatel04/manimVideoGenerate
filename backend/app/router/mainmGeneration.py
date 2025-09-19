from fastapi import (
    APIRouter, 
    status, 
    HTTPException,
    Depends
)
from app.schema.manimGenerationSchema import MainmUserModel, CancelRequest
from app.services.manim.manim import call_graph
# from app.services.task import call_graph
from fastapi.responses import StreamingResponse
from app.utils.auth import getCurrentUser
from celery.result import AsyncResult
from app.core.queue import taskQueue
from app.models.UserHistory import UsersHistory
from app.core.redis import get_queue_length
import json

router = APIRouter(
    prefix="/api/manimGeneration"
)

# @router.post("/generate", status_code=status.HTTP_201_CREATED)
# async def generateManimVideo(query: MainmUserModel):
#     async def event_generator():
#         async for event in call_graph(query.userQuery):
#             yield f"data: {json.dumps(event)}\n\n"
#         yield "event: end\ndata: [DONE]\n\n"
#     return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def generate(query: MainmUserModel, userId: int=Depends(getCurrentUser)):

    historyId = getattr(query, "historyId", None)
    task = call_graph.apply_async(
        args=[
            query.userQuery,
            userId.id,query.quality,
            query.format, 
            historyId
        ]
    )
    return {"task_id": task.id}

@router.post("/cancel", status_code=status.HTTP_202_ACCEPTED)
async def cancel_task(req: CancelRequest,  userId: int = Depends(getCurrentUser)):
    taskQueue.control.revoke(req.taskId, terminate=True, signal="SIGKILL")
    return {"status": "revoked", "taskId": req.taskId}


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
            "timestamp": result.info.get('timestamp'),

        }
    elif result.state == 'SUCCESS':
        return {
            "status": "completed",
            "state": result.state,
            "data": result.result,
        }
    elif result.state == 'FAILURE':
        return {
            "status": "failed",
            "state": result.state,
            "error": str(result.info),
        }
    elif result.state == 'REVOKED':
        return {
            "status": "cancelled",
            "state": result.state,
            "message": "Task was cancelled by user",
        }
    else:
        queue_length = get_queue_length()
        return {
            "status": "pending",
            "state": result.state,
            "queue_left": queue_length
        }