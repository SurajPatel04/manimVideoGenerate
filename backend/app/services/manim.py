from app.schema.ServiceSchema import (
    DescriptionGenerationState, 
    mainmState
)
from app.services.graphForDescriptionGenerate import graph_for_description_generate 
from app.services.graphForManimCodeGenerate import graph_for_mainm_code_generate
from app.core.queue import taskQueue
from app.models.UserHistory import Message


@taskQueue.task(name="call_graph_task")
def call_graph(query):
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

    result = graph_for_description_generate.invoke(state)

    if result.get("isFesiable") is False:
        return "Not possible"

    print(result)

    stat1 = mainmState(
        description= result.get("detailedDescription"),
        isCodeGood=None,
        format=state.format,
        error_message="",
        rewriteAttempts=0,
        filename="",
        executionSuccess = None,
        quality = "ql",
        createAgain = 0
    )

    manimGeneration = graph_for_mainm_code_generate.invoke(stat1)

    code = manimGeneration.get('code')
    userQuery = query
    description = manimGeneration.get('description')
    quality = manimGeneration.get('quality')


    # message = Message(
    #     userQuery=query,
    #     AiResponse=result.get("detailedDescription"),
    #     code: 

    # )
    print("___________last Message__________")
    print(f"Description: {description}")
    print(f"Filename: {manimGeneration.get('filename')}")
    print(f"Is Code Good: {manimGeneration.get('isCodeGood')}")
    print(f"Execution Success: {manimGeneration.get('executionSuccess')}")
    print(f"Rewrite Attempts: {manimGeneration.get('rewriteAttempts')}")
    print(f"Quality: {quality}")
    print(f"Format: {manimGeneration.get('format')}")
    print(f"Code: {code}")
    # if hasattr(manimGeneration, 'code'):
    #     print(f"Code Length: {len(manimGeneration.code) if manimGeneration.code else 0} characters")
    # if hasattr(manimGeneration, 'validationError') and manimGeneration.validationError:
    #     print(f"Validation Error: {manimGeneration.validationError}")
    # if hasattr(manimGeneration, 'executionError') and manimGeneration.executionError:
    #     print(f"Execution Error: {manimGeneration.executionError}")
    
    # # Print full state as dict (might be long)
    # print("___________Complete State as Dict__________")
    # if hasattr(manimGeneration, '__dict__'):
    #     import pprint
    #     pprint.pprint(vars(manimGeneration))

    return (manimGeneration)