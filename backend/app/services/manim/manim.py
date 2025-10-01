from app.schema.ServiceSchema import (
    DescriptionGenerationState, 
    mainmState,
    isQueryPossible
)
from app.services.manim.graphForDescriptionGenerate import graph_for_description_generate 
from app.services.manim.graphForManimCodeGenerate import graph_for_mainm_code_generate
from app.services.manim.graphForFesibilityCheck import graph_for_query_fesibility_check
from app.core.queue import taskQueue
from app.models.UserHistory import Message, UsersHistory
from app.core.db import init_beanie_for_workers, close_worker_db
from bson import ObjectId
import asyncio
from datetime import datetime
import os
import shutil
from app.utils.supabaseClient import uploadFile
from app.schema.ServiceSchema import AnimationType

@taskQueue.task(name="call_graph_task", bind=True)
def call_graph(self, query, userID, quality, format, historyId=None, resolution="1920x1080"):
    async def _inner():
        try:
            await init_beanie_for_workers()
            
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
                update_progress("Checking Feasibility", 20, "Analyzing if user query is possible")
                print(f"DEBUG: About to check feasibility for query: {query}")

                fesibleState = isQueryPossible(
                    userQuery=query,
                    chatName=None,
                    animationType=None,
                )
                print(f"DEBUG: Created feasibility state: {fesibleState}")

                fesibleResult = graph_for_query_fesibility_check.invoke(fesibleState)
                print(f"DEBUG: Feasibility check result: {fesibleResult}")
            
                is_feasible = fesibleResult.get("isFeasible")
                # print(f"DEBUG: Extracted feasibility value: {is_feasible}")
                
                if is_feasible is False:
                    print(f"DEBUG: STOPPING EXECUTION - Query not feasible: {fesibleResult.get('reason')}")
                    update_progress("Failed", 100, f"Not feasible: {fesibleResult.get('reason', 'Unknown reason')}")
                    return {
                        "success": False,
                        "message": "Not possible",
                        "reason": fesibleResult.get('reason'),
                        "stage": "feasibility_check"
                    }
                
                print(f"DEBUG: CONTINUING EXECUTION - Query is feasible")
                update_progress("Description Generation", 30, f"Chat name: {fesibleResult.get('chatName')}")
                
                print(f"DEBUG: CONTINUING EXECUTION - Query is feasible")
                update_progress("Description Generation", 30, f"Chat name: {fesibleResult.get('chatName')}")
                
                descriptionState=DescriptionGenerationState(
                    userQuery=query,
                    descriptions=[],
                    detailedDescription="",
                    descriptionRefine=0,
                    AutoComplete=True,
                    isGood=None,
                    detailedDescriptionError= None,
                    format = format,
                    chatName=fesibleResult.get('chatName'),
                    reason=fesibleResult.get('reason'),
                    animationType=fesibleResult.get("animationType"),
                )



                update_progress("Generating Description", 30, "Detailed description in progress")
                
                result = await graph_for_description_generate.ainvoke(descriptionState)

                update_progress("Generating Manim Code", 50, "Creating animation code")
                manimGenerationState = mainmState(
                    description= result.get("detailedDescription"),
                    isCodeGood=None,
                    format=descriptionState.format,
                    error_message="",
                    rewriteAttempts=0,
                    filename="",
                    executionSuccess = None,
                    quality = quality,
                    createAgain = 0,
                    animationType=fesibleResult.get("animationType"),
                    resolution=resolution
                )

                manimGeneration = await graph_for_mainm_code_generate.ainvoke(manimGenerationState)

                code = manimGeneration.get('code')
                userQuery = query
                description = manimGeneration.get('description')
                generated_quality = manimGeneration.get('quality')

                filename_without_extension = manimGeneration.get("filename").replace(".py", "")
                link = uploadFile(filename_without_extension, manimGeneration.get("format"))

                
                try:
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    backend_dir = os.path.dirname(os.path.dirname(current_dir))
                    
                    video_file_path_with_suffix = os.path.join(backend_dir, "videos", f"{filename_without_extension}_ManimCE_v0.19.0.{manimGeneration.get('format')}")
                    video_file_path_without_suffix = os.path.join(backend_dir, "videos", f"{filename_without_extension}.{manimGeneration.get('format')}")
                    
                    if os.path.exists(video_file_path_with_suffix):
                        os.remove(video_file_path_with_suffix)
                        # print(f"Successfully removed video file: {video_file_path_with_suffix}")
                    elif os.path.exists(video_file_path_without_suffix):
                        os.remove(video_file_path_without_suffix)
                        # print(f"Successfully removed video file: {video_file_path_without_suffix}")
                    else:
                        print(f"Video file not found for cleanup: {video_file_path_with_suffix} or {video_file_path_without_suffix}")
                    
                    # Remove the partial movie files directory
                    partial_movie_dir = os.path.join(backend_dir, "videos", "partial_movie_files", filename_without_extension)
                    if os.path.exists(partial_movie_dir):
                        shutil.rmtree(partial_movie_dir)
                        print(f"Successfully removed partial movie files directory: {partial_movie_dir}")
                    else:
                        print(f"Partial movie files directory not found for cleanup: {partial_movie_dir}")
                        
                except Exception as cleanup_error:
                    print(f"Warning: Failed to remove files during cleanup: {cleanup_error}")

                message = Message(
                    userQuery=query,
                    description=result.get("detailedDescription"),
                    code=code,
                    quality=generated_quality,
                    filename=filename_without_extension,
                    link=link
                )

                if historyId:
                    existing_history = await UsersHistory.get(ObjectId(historyId))
                    if existing_history:
                        existing_history.messages.append(message)
                        await existing_history.save()
                        history = existing_history
                    else:
                        history = UsersHistory(
                            userId=ObjectId(userID),
                            chatName=fesibleResult.get("chatName"),
                            messages=[message]
                        )
                        await history.insert()
                    history_id = str(history.id)
                else:
                    history = UsersHistory(
                        userId=ObjectId(userID),
                        chatName=fesibleResult.get("chatName"),
                        messages=[message]
                    )
                    await history.insert()
                    history_id = str(history.id)

                update_progress("Completed", 100, "Video generation completed successfully")
                
                return {
                    "success": True,
                    "link": link,
                    "historyId": history_id,
                    "data": manimGeneration,
                    "chat_name": result.get("chatName"),
                    "description": result.get("detailedDescription"),
                    "quality": generated_quality,
                    "code": code,
                }
                
            except Exception as e:
                error_msg = str(e)
                update_progress("Error", 100, f"An error occurred: {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "stage": "unknown"
                }
        finally:
            try:
                await close_worker_db()
            except Exception as cleanup_error:
                print(f"Warning: Failed to close database connection: {cleanup_error}")
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(_inner())