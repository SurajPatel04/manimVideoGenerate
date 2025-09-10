from app.schema.ServiceSchema import (
    DescriptionGenerationState, 
    mainmState
)
from app.services.graphForDescriptionGenerate import graph_for_description_generate 
from app.services.graphForManimCodeGenerate import graph_for_mainm_code_generate



async def call_graph(query):
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
        format = "mp4",
        isFesible=None,
        chatName=None,
        reason=None
    )

    final_state = None
    async for event in graph_for_description_generate.astream(state):
        final_state=event
        yield event

    if final_state.get("validateDescription").get("isFesible") is False:
        print("Request not feasible with Manim. Stopping here.")
        return

    stat1 = mainmState(
        description=final_state.get("validateDescription").get("detailedDescription"),
        isCodeGood=None,
        format=state.format,
        error_message="",
        rewriteAttempts=0,
        filename="",
        executionSuccess = None,
        quality = "ql",
        createAgain = 0
    )

    async for event in graph_for_mainm_code_generate.astream(stat1):
        yield event
