from graphForDescriptionGenerate import graph_for_description_generate 
from schema import DescriptionGenerationState, mainmState
from graphForManimCodeGenerate import graph_for_mainm_code_generate



def call_graph():
    query = input("Enter your query for video generation: ")
    state=DescriptionGenerationState(
        userQuery=query,
        descriptions=[],
        pickedOne="",
        DescriptionRefine=0,
        AutoComplete=True,
        isGood=None,
        pickedOneError= None,
        format = "mp4",
        isFesible=None,
        chatName=None,
        reason=None
    )

    
    result = graph_for_description_generate .invoke(state)
    if result.get("isFesible") is False:
        print("❌ Request not feasible with Manim. Stopping here.")
        return
    stat1 = mainmState(
        description=result.get("pickedOne"),
        isCodeGood=None,
        format=state.format,
        error_message="",
        rewriteAttempts=0,
        filename="",
        executionSuccess = None,
        quality = "ql",
        createAgain = 0
    )
    result = graph_for_mainm_code_generate.invoke(stat1)
    print(result)

call_graph()