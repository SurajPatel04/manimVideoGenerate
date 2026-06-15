from langgraph.graph import (
    StateGraph, 
    START, 
    END
)
from app.services.manim.manimCodeGeneration import (
    staticCheckCode, 
    generateInitialCode, 
    fixCodeErrorsWithLLM, 
    testRenderCode, 
    productionRender,
    verifyOutputMatchesDescription,
    manimRouter,executionRouter, matchRouter,
    shouldStartOverRouter, 
    handleFailureAndReset
)
from app.schema.ServiceSchema import mainmState

graph_build = StateGraph(mainmState)

graph_build.add_node("Generate_Initial_Code", generateInitialCode)
graph_build.add_node("Syntax_And_Deprecation_Check", staticCheckCode)
graph_build.add_node("Fix_Code_Errors_With_LLM", fixCodeErrorsWithLLM)
graph_build.add_node("Test_Render_Code", testRenderCode)
graph_build.add_node("Vision_QA_Output", verifyOutputMatchesDescription)
graph_build.add_node("Final_High_Quality_Render", productionRender)
graph_build.add_node("Handle_Failure_And_Reset", handleFailureAndReset)


graph_build.add_edge(START, "Generate_Initial_Code")
graph_build.add_edge("Generate_Initial_Code", "Syntax_And_Deprecation_Check")
graph_build.add_edge("Fix_Code_Errors_With_LLM", "Syntax_And_Deprecation_Check")

graph_build.add_conditional_edges(
    "Syntax_And_Deprecation_Check",
    manimRouter,
    {
        "testRenderCode": "Test_Render_Code",
        "fixCodeErrorsWithLLM": "Fix_Code_Errors_With_LLM",
        "limit_reached": "Handle_Failure_And_Reset",
    },
)

graph_build.add_conditional_edges(
    "Test_Render_Code",
    executionRouter,
    {
        "fix": "Fix_Code_Errors_With_LLM",        
        "done": "Vision_QA_Output", 
        "limit": "Handle_Failure_And_Reset",
    },
)

graph_build.add_conditional_edges(
    "Vision_QA_Output",
    matchRouter,
    {
        "render": "Final_High_Quality_Render",
        "fix": "Fix_Code_Errors_With_LLM",
        "limit": "Handle_Failure_And_Reset",
    },
)

graph_build.add_conditional_edges(
    "Handle_Failure_And_Reset",
    shouldStartOverRouter,
    {
        "generateInitialCode": "Generate_Initial_Code",
        "stop": END,
    },
)


graph_build.add_edge("Final_High_Quality_Render", END)
graph_for_mainm_code_generate = graph_build.compile()