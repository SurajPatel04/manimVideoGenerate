from langgraph.graph import StateGraph, START, END
from schema import mainmState
from manimCodeGeneration import agentCheckFileCode, agentCreateFile, agentReWriteManimCode, agentRunManimCode, manimRouter,executionRouter, shouldStartOverRouter, handleFailureAndReset

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
        END: "handleFailureAndReset",
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
        END: END,
    },
)

graph_for_mainm_code_generate = graph_build.compile()