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
                    userQuery=query,
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
                    import glob
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    # current_dir is backend/app/services/manim
                    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
                    videos_dir = os.path.join(backend_dir, "videos")
                    
                    # Remove ALL files in videos/ that start with the animation name
                    # This catches: production renders (_ManimCE_vX.X.X.mp4), check renders (.mp4), extracted frames (_frame_N.jpg)
                    for f in glob.glob(os.path.join(videos_dir, f"{filename_without_extension}*")):
                        if os.path.isfile(f):
                            os.remove(f)
                            print(f"Cleanup: removed {os.path.basename(f)}")
                    
                    # Remove the partial_movie_files directory for this animation
                    partial_movie_dir = os.path.join(videos_dir, "partial_movie_files", filename_without_extension)
                    if os.path.exists(partial_movie_dir):
                        shutil.rmtree(partial_movie_dir)
                        print(f"Cleanup: removed partial_movie_files/{filename_without_extension}")
                    
                    # Remove the temp_files directory for this animation (if it exists)
                    temp_files_dir = os.path.join(videos_dir, "temp_files")
                    if os.path.exists(temp_files_dir):
                        for f in glob.glob(os.path.join(temp_files_dir, f"{filename_without_extension}*")):
                            if os.path.isfile(f):
                                os.remove(f)
                    
                    # Remove the source .py file from temp/
                    temp_py = os.path.join(backend_dir, "temp", f"{filename_without_extension}.py")
                    if os.path.exists(temp_py):
                        os.remove(temp_py)
                        print(f"Cleanup: removed temp/{filename_without_extension}.py")
                        
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
                import traceback
                error_msg = str(e)
                print(f"call_graph failed:\n{traceback.format_exc()}")
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