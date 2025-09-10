from langgraph.graph import (
    StateGraph, 
    START, 
    END
)
from app.services.manimCodeGeneration import (
    agentCheckFileCode, 
    agentCreateFile, 
    agentReWriteManimCode, 
    agentRunManimCode, 
    manimRouter,executionRouter, 
    shouldStartOverRouter, 
    handleFailureAndReset
)
from app.schema.ServiceSchema import mainmState

graph_build = StateGraph(mainmState)

graph_build.add_node("agentCreateFile", agentCreateFile)
graph_build.add_node("agentCheckFileCode", agentCheckFileCode)
graph_build.add_node("agentReWriteManimCode", agentReWriteManimCode)
graph_build.add_node("agentRunManimCode", agentRunManimCode)
graph_build.add_node("handleFailureAndReset", handleFailureAndReset)


graph_build.add_edge(START, "agentCreateFile")
graph_build.add_edge("agentCreateFile", "agentCheckFileCode")
graph_build.add_edge("agentReWriteManimCode", "agentCheckFileCode")

graph_build.add_conditional_edges(
    "agentCheckFileCode",
    manimRouter,
    {
        "agentRunManimCode": "agentRunManimCode",
        "agentReWriteManimCode": "agentReWriteManimCode",
        "limit_reached": "handleFailureAndReset",
    },
)

graph_build.add_conditional_edges(
    "agentRunManimCode",
    executionRouter,
    {
        "fix": "agentReWriteManimCode",        
        "done": END, 
        "limit": "handleFailureAndReset",
    },
)

graph_build.add_conditional_edges(
    "handleFailureAndReset",
    shouldStartOverRouter,
    {
        "agentCreateFile": "agentCreateFile", 
        "stop": END,
    },
)

graph_for_mainm_code_generate = graph_build.compile()