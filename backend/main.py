from graphForDescriptionGenerate import graph_for_description_generate 
from schema import DescriptionGenerationState, mainmState
from graphForManimCodeGenerate import graph_for_mainm_code_generate

def call_graph():
    state=DescriptionGenerationState(
        user_query="Genertae video of Hello World in 10 diffent-diffent language like ('Hindi', 'tamil' etc.)  with good animation",
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
        quality = "ql"
    )
    print("******************* state1 description***********", stat1.description)
    result = graph_for_mainm_code_generate.invoke(stat1)
    print(result)

for i in range(1):
    print("Running times: ",i+1)
    call_graph()