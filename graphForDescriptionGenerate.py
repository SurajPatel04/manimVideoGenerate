from schema import DescriptionGenerationState
from langgraph.graph import StateGraph, START, END
from descriptionGenerate import  generateDetailedDescription, validateDescription,refineDescription, router

graph_build = StateGraph(DescriptionGenerationState)
# graph_build.add_node("generateMultipleDescription", generateMultipleDescription)
graph_build.add_node("generateDetailedDescription", generateDetailedDescription)
graph_build.add_node("validateDescription", validateDescription)
graph_build.add_node("refineDescription", refineDescription)


# graph_build.add_edge(START, "generateMultipleDescription")
graph_build.add_edge(START, "generateDetailedDescription")
graph_build.add_edge("generateDetailedDescription", "validateDescription")
graph_build.add_conditional_edges("validateDescription",router)
graph_build.add_edge("refineDescription", "validateDescription")

graph_for_description_generate = graph_build.compile()