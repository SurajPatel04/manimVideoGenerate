from app.schema.ServiceSchema import (
    DescriptionGenerationState, 
    mainmState
)
from app.services.graphForDescriptionGenerate import graph_for_description_generate 
from app.services.graphForManimCodeGenerate import graph_for_mainm_code_generate
from app.core.queue import taskQueue
from app.models.UserHistory import Message, UsersHistory
from app.core.db import init_beanie_for_workers
from bson import ObjectId
import asyncio
from datetime import datetime
import time

_beanie_initialized = False

async def ensure_beanie_initialized():
    """Ensure Beanie is initialized for Celery workers"""
    global _beanie_initialized
    if not _beanie_initialized:
        await init_beanie_for_workers()
        _beanie_initialized = True


@taskQueue.task(name="call_graph_task", bind=True)
def call_graph(self, query, userID, quality, format):
    async def _inner():
        await ensure_beanie_initialized()
        
        def update_progress(stage, progress_percent, details=None):
            self.update_state(
                state='PROGRESS',
                meta={
                    'current_stage': stage,
                    'progress': progress_percent,
                    'details': details,
                    'timestamp': datetime.now().isoformat()
                }
            )
        
        try:
            update_progress("Initializing", 10, "Setting up description generation state")
            
            state=DescriptionGenerationState(
                userQuery=query,
                descriptions=[],
                detailedDescription="",
                descriptionRefine=0,
                currentStage="isUserQueryPossible",
                nextStage=None,
                AutoComplete=True,
                isGood=None,
                detailedDescriptionError= None,
                format = format,
                isFesible=None,
                chatName=None,
                reason=None
            )

            update_progress("Checking Feasibility", 20, "Analyzing if user query is possible")
            time.sleep(5) 

            update_progress("Generating Description", 30, "Detailed description in progress")
            
            result = graph_for_description_generate.invoke(state)

            if result.get("isFesiable") is False:
                update_progress("Failed", 100, f"Not feasible: {result.get('reason', 'Unknown reason')}")
                return {
                    "success": False,
                    "message": "Not possible",
                    "reason": result.get('reason'),
                    "stage": "feasibility_check"
                }

            # Stage 3: Description generated (60% complete)
            update_progress("Description Generated", 40, f"Chat name: {result.get('chatName')}")
            print(result)

            # Stage 4: Generate Manim code (80% complete)
            update_progress("Generating Manim Code", 50, "Creating animation code")
            
            stat1 = mainmState(
                description= result.get("detailedDescription"),
                isCodeGood=None,
                format=state.format,
                error_message="",
                rewriteAttempts=0,
                filename="",
                executionSuccess = None,
                quality = quality,
                createAgain = 0
            )

            manimGeneration = graph_for_mainm_code_generate.invoke(stat1)

            code = manimGeneration.get('code')
            userQuery = query
            description = manimGeneration.get('description')
            generated_quality = manimGeneration.get('quality')


            message = Message(
                userQuery=query,
                description=result.get("detailedDescription"),
                code=code,
                quality=generated_quality
            )

            history=UsersHistory(
                userId=ObjectId(userID),
                chatName=result.get("chatName"),
                messages=[message]
            )

            await history.insert()
            
            # Stage 6: Complete (100%)
            update_progress("Completed", 100, "Video generation completed successfully")
            
            return {
                "success": True,
                "data": manimGeneration,
                "chat_name": result.get("chatName"),
                "description": result.get("detailedDescription"),
                "quality": generated_quality,
                "code": code
            }
            
        except Exception as e:
            error_msg = str(e)
            update_progress("Error", 100, f"An error occurred: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "stage": "unknown"
            }
    return asyncio.run(_inner())