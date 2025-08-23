from graphForDescriptionGenerate import graph_for_description_generate 
from schema import DescriptionGenerationState, mainmState
from graphForManimCodeGenerate import graph_for_mainm_code_generate



def call_graph():
    query = input("Enter your query for video generation: ")
    state=DescriptionGenerationState(
        user_query=query,
        descriptions=[],
        pickedOne="",
        DescriptionRefine=0,
        AutoComplete=True,
        is_good=None,
        pickedOneError= None
    )

    
    result = graph_for_description_generate .invoke(state)

    stat1 = mainmState(
        description=result.get("pickedOne"),
        is_code_good=None,
        error_message="",
        rewrite_attempts=0,
        filename="",
        execution_success = None,
        quality = "ql",
        create_again = 0
    )
    result = graph_for_mainm_code_generate.invoke(stat1)
    print(result)

call_graph()